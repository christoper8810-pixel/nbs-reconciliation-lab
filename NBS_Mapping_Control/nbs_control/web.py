"""Local owner review interface (Flask, 127.0.0.1 only).

Views: dashboard, proposed rules, owner decisions, effective rules, unresolved
items, findings queue, sections, configuration (versioned edit + restore),
exports, ECB review run. All state changes are POSTs with a CSRF token and an
explicit owner name, reason and (for approvals) date and evidence.
"""

from __future__ import annotations

import json
import secrets
from pathlib import Path
from typing import Any

from flask import Flask, abort, flash, redirect, render_template, request, send_from_directory, session, url_for

from . import EXPORT_DIR
from .config import CONFIG_NAMES, ConfigError, config_history, config_path, parse_json, restore_config, save_config
from .exports import BANK_INPUTS, export_all, rule_text
from .store import ACTIONS, DecisionError

PAGE_SIZE = 100


def create_app(service, export_dir: Path = EXPORT_DIR) -> Flask:
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32)
    app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024
    app.jinja_env.globals.update(rule_text=rule_text, json=json, ACTIONS=ACTIONS)

    @app.before_request
    def csrf() -> None:
        session.setdefault("csrf", secrets.token_hex(16))
        if request.method == "POST" and request.form.get("csrf") != session["csrf"]:
            abort(400, "Missing or invalid CSRF token")

    @app.context_processor
    def inject() -> dict[str, Any]:
        return {"csrf_token": session.get("csrf", "")}

    def _form_decision() -> dict[str, Any]:
        return {"actor": request.form.get("actor", ""), "reason": request.form.get("reason", ""),
                "approved_on": request.form.get("approved_on") or None,
                "approval_evidence": request.form.get("approval_evidence") or None}

    def _catalog_or_setup():
        if service.store.current_catalog() is None:
            return redirect(url_for("setup"))
        return None

    @app.route("/setup", methods=["GET", "POST"])
    def setup():
        if request.method == "POST":
            try:
                if request.form.get("mode") == "supplied":
                    result = service.refresh(use_supplied_inventory=True, note=request.form.get("note", ""))
                else:
                    paths = {"T24": Path(request.form["t24"].strip().strip('"')),
                             "ETHIX": Path(request.form["ethix"].strip().strip('"'))}
                    result = service.refresh(paths, note=request.form.get("note", ""))
                changes = result["changes"] or {}
                flash(f"Imported catalog v{result['catalog_version']}: {result['mapping_count']} rows; "
                      f"changed {len(changes.get('changed', []))}, added {len(changes.get('added', []))}, "
                      f"removed {len(changes.get('removed', []))}; stale/orphaned decisions: "
                      f"{result['stale_or_orphaned_decisions']}", "ok")
                return redirect(url_for("dashboard"))
            except (FileNotFoundError, ValueError, ConfigError, OSError) as exc:
                flash(f"Import failed: {exc}", "error")
        from . import DEFAULT_SOURCES
        return render_template("setup.html", defaults=DEFAULT_SOURCES, versions=service.store.catalog_versions())

    @app.route("/")
    def dashboard():
        if (r := _catalog_or_setup()):
            return r
        return render_template("dashboard.html", summary=service.summary(), versions=service.store.catalog_versions(),
                               global_items=service.global_open_items())

    @app.route("/mappings")
    def mappings():
        if (r := _catalog_or_setup()):
            return r
        view = request.args.get("view", "proposed")
        system = request.args.get("system", "")
        query = request.args.get("q", "").strip().lower()
        state = request.args.get("state", "")
        page = max(1, int(request.args.get("page", 1) or 1))
        evaluations = service.evaluations()
        rows = []
        for e in evaluations:
            item = e["item"]
            if view == "proposed" and item["proposal"]["status"] != "PROPOSED":
                continue
            if view == "rules" and item["kind"] != "RULE":
                continue
            if view == "effective" and e["state"] != "EFFECTIVE":
                continue
            if view == "unresolved" and not ((item["kind"] == "RULE" and e["state"] not in ("EFFECTIVE", "REJECT", "NOT_APPLICABLE"))
                                             or e["state"] in ("STALE", "APPROVED_BLOCKED")):
                continue
            if view == "decided" and e["decision"] is None:
                continue
            if system and item["source_system"] != system:
                continue
            if state and e["state"] != state:
                continue
            if query and query not in " ".join(str(x) for x in (item["business_id"], item["sheet"], item["hierarchy_path"],
                                                                  rule_text(item), item["proposal"].get("metric_expression"))).lower():
                continue
            rows.append(e)
        sort = request.args.get("sort", "source")
        keys = {"source": lambda e: (e["item"]["source_system"], e["item"]["sheet"], e["item"]["source_row"]),
                "state": lambda e: (e["state"], e["item"]["business_id"]),
                "id": lambda e: e["item"]["business_id"]}
        rows.sort(key=keys.get(sort, keys["source"]))
        total = len(rows)
        rows = rows[(page - 1) * PAGE_SIZE: page * PAGE_SIZE]
        states = sorted({e["state"] for e in evaluations})
        return render_template("mappings.html", rows=rows, view=view, system=system, q=query, state=state, states=states,
                               page=page, total=total, pages=max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE), sort=sort)

    @app.route("/mapping/<business_id>", methods=["GET", "POST"])
    def mapping(business_id: str):
        if (r := _catalog_or_setup()):
            return r
        try:
            item = service.mapping(business_id)
        except KeyError:
            abort(404)
        if request.method == "POST":
            form = _form_decision()
            try:
                if request.form.get("rollback_to"):
                    service.store.rollback("MAPPING", business_id, int(request.form["rollback_to"]), form["actor"], form["reason"])
                    flash("Rolled back (new history entry recorded)", "ok")
                else:
                    spec: dict[str, Any] = {}
                    for key in ("metric_expression", "amount_basis", "exclusive_group", "effective_from", "effective_to"):
                        if request.form.get(key, "").strip():
                            spec[key] = request.form[key].strip()
                    if request.form.get("selectors", "").strip():
                        spec["selectors"] = parse_json(request.form["selectors"])
                    targets = request.form.getlist("nbs_target_business_ids")
                    if targets:
                        spec["nbs_target_business_ids"] = targets
                    service.decide_mapping(business_id, request.form["action"], spec=spec or None, **form)
                    flash("Decision recorded", "ok")
            except (DecisionError, ConfigError, ValueError) as exc:
                flash(f"Not recorded: {exc}", "error")
            return redirect(url_for("mapping", business_id=business_id))
        evaluation = service.evaluate(item)
        history = service.store.history("MAPPING", business_id)
        findings = [f for f in service.catalog["findings_queue"] if f["business_id"] == business_id]
        policy = service.config["calculation_policy"]
        return render_template("mapping.html", item=item, evaluation=evaluation, history=history, findings=findings,
                               metrics=policy["metrics"], bases=list(policy["amount_bases"]),
                               fields=service.config["report_selectors"]["fields"])

    @app.route("/decisions")
    def decisions():
        if (r := _catalog_or_setup()):
            return r
        return render_template("decisions.html", rows=service.decision_rows(), history=service.store.history(limit=200))

    @app.route("/unresolved")
    def unresolved():
        if (r := _catalog_or_setup()):
            return r
        view = service.unresolved_view()
        counts: dict[str, int] = {}
        for e in view["mappings"]:
            for reason in e["reasons"] or [e["state"]]:
                key = reason.split(":")[0]
                counts[key] = counts.get(key, 0) + 1
        return render_template("unresolved.html", view=view, reason_counts=sorted(counts.items(), key=lambda kv: -kv[1]))

    @app.route("/findings", methods=["GET", "POST"])
    def findings():
        if (r := _catalog_or_setup()):
            return r
        if request.method == "POST":
            try:
                service.decide_finding(request.form["item_id"], request.form["action"], **_form_decision())
                flash("Finding decision recorded", "ok")
            except (DecisionError, KeyError) as exc:
                flash(f"Not recorded: {exc}", "error")
            return redirect(url_for("findings", _anchor=request.form.get("item_id", "")))
        current = service.store.current_all("FINDING")
        rows = []
        for entry in service.catalog["findings_queue"]:
            decision = current.get(entry["item_id"])
            rows.append({"entry": entry, "decision": decision, "validity": service.validity(decision, entry["fingerprint"])})
        return render_template("findings.html", rows=rows, findings_meta=service.config["finding_classification"])

    @app.route("/sections", methods=["GET", "POST"])
    def sections():
        if (r := _catalog_or_setup()):
            return r
        if request.method == "POST":
            try:
                service.decide_section(request.form["section_id"], request.form["action"],
                                       block_keys=request.form.getlist("block_keys"), **_form_decision())
                flash("Section decision recorded", "ok")
            except (DecisionError, KeyError) as exc:
                flash(f"Not recorded: {exc}", "error")
            return redirect(url_for("sections"))
        current = service.store.current_all("SECTION")
        rows = [{"section": s, "decision": current.get(s["section_id"]),
                 "validity": service.validity(current.get(s["section_id"]), s["fingerprint"])}
                for s in service.catalog["sections"]]
        return render_template("sections.html", rows=rows)

    @app.route("/config", methods=["GET"])
    def config_index():
        return render_template("config_index.html", names=CONFIG_NAMES, history=list(reversed(config_history(service.config_dir))),
                               hashes=service.config.hashes())

    @app.route("/config/<name>", methods=["GET", "POST"])
    def config_edit(name: str):
        if name not in CONFIG_NAMES:
            abort(404)
        text = None
        if request.method == "POST":
            try:
                if request.form.get("restore"):
                    restore_config(name, request.form["restore"], request.form.get("actor", ""), request.form.get("reason", ""),
                                   service.config_dir)
                else:
                    text = request.form["text"]
                    save_config(name, text, request.form.get("actor", ""), request.form.get("reason", ""), service.config_dir)
                service.reload_config()
                flash(f"{name} saved as a new version. Proposals refresh on the next import.", "ok")
                return redirect(url_for("config_edit", name=name))
            except (ConfigError, ValueError) as exc:
                flash(f"Not saved: {exc}", "error")
        if text is None:
            text = config_path(name, service.config_dir).read_text(encoding="utf-8")
        versions = sorted((p.name.split(".")[1] for p in (service.config_dir / "history").glob(f"{name}.*.json")), reverse=True)
        return render_template("config_edit.html", name=name, text=text, versions=versions)

    @app.route("/exports", methods=["GET", "POST"])
    def exports():
        if (r := _catalog_or_setup()):
            return r
        if request.method == "POST":
            written = export_all(service, Path(export_dir))
            flash("Exports written: " + ", ".join(Path(p).name for p in written.values()), "ok")
            return redirect(url_for("exports"))
        files = sorted(p.name for p in Path(export_dir).glob("*") if p.is_file()) if Path(export_dir).exists() else []
        return render_template("exports.html", files=files, bank_inputs=BANK_INPUTS)

    @app.route("/exports/download/<path:name>")
    def download(name: str):
        return send_from_directory(Path(export_dir).resolve(), name, as_attachment=True)

    @app.route("/exports/import", methods=["POST"])
    def import_workbook():
        from .exports import import_owner_workbook
        upload = request.files.get("workbook")
        if upload is None or not upload.filename.lower().endswith(".xlsx"):
            flash("Choose an exported .xlsx owner review workbook", "error")
            return redirect(url_for("exports"))
        target = service.store.data_dir / "uploads"
        target.mkdir(exist_ok=True)
        path = target / f"owner-review-{secrets.token_hex(6)}.xlsx"
        upload.save(path)
        try:
            result = import_owner_workbook(service, path, request.form.get("actor") or None)
            flash(f"Applied {len(result['applied'])} decisions; {len(result['errors'])} rows refused", "ok" if not result["errors"] else "error")
            for error in result["errors"][:20]:
                flash(f"Row {error['row']} {error['business_id']}: {error['error']}", "error")
        except ValueError as exc:
            flash(f"Import failed: {exc}", "error")
        return redirect(url_for("exports"))

    @app.route("/run", methods=["GET", "POST"])
    def run():
        result = None
        if request.method == "POST":
            from .ecb_adapter import run_review
            upload = request.files.get("payload")
            try:
                if upload is None or not upload.filename:
                    raise ValueError("Choose an ECB JSON export")
                payload = parse_json(upload.read().decode("utf-8-sig"))
                result = run_review(payload, service.rules, service.config["balance_rules"],
                                    service.config["calculation_policy"], service.config["report_selectors"])
            except (ValueError, ConfigError, UnicodeDecodeError) as exc:
                flash(f"Run failed: {exc}", "error")
        return render_template("run.html", result=result)

    from .report_web import register_report_routes
    register_report_routes(app,service,export_dir)
    from .rebuild_web import register_rebuild_routes
    register_rebuild_routes(app,service.config_dir.parent)
    from .tbrecon.web import register_tb_routes
    register_tb_routes(app, service.config_dir.parent)
    return app
