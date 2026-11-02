"""Application service: refresh, owner decisions and the four review views.

Effective = explicit owner approval + current evidence + validated structured
selectors on approved fields + available metrics + approved amount basis +
resolved section/block/finding dependencies. Everything else is unresolved.
Approval is application state, never proof of bank reconciliation.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from . import CONFIG_DIR, DATA_DIR, DEFAULT_SOURCES, PROJECT_ROOT
from . import catalog as catalog_mod
from . import importer
from .config import ConfigSet
from .report_calc import metric_status
from .selectors import SelectorError, compile_selector, parse_expression, validate_selector
from .store import DecisionError, Store

SUPPLIED_DIR = PROJECT_ROOT
RESOLVED_FINDING_ACTIONS = {"CORRECTION_APPROVED", "POLICY_DECIDED", "ACCEPT_LEGACY", "NOT_A_DEFECT"}
SPEC_KEYS = ("metric_expression", "selectors", "amount_basis", "exclusive_group", "effective_from", "effective_to",
             "source_fields", "nbs_target_business_ids", "dependencies_acknowledged")


class ControlService:
    def __init__(self, config_dir: str | Path = CONFIG_DIR, data_dir: str | Path = DATA_DIR,
                 supplied_dir: str | Path = SUPPLIED_DIR):
        self.config_dir = Path(config_dir)
        self.supplied_dir = Path(supplied_dir)
        self.store = Store(data_dir)
        self.reload_config()

    def reload_config(self) -> None:
        self.config = ConfigSet(self.config_dir)
        self.rules = self.config.engine_rules

    # ---- refresh ----------------------------------------------------------
    def refresh(self, paths: dict[str, str | Path] | None = None, use_supplied_inventory: bool = False,
                note: str = "") -> dict[str, Any]:
        """Re-import evidence, rebuild the catalog and report decisions invalidated by changes."""
        self.reload_config()
        if use_supplied_inventory:
            imports = importer.inventory_from_supplied(self.supplied_dir / "source_inventory.json",
                                                       self.supplied_dir / "source_manifest.json")
        else:
            imports = importer.import_sources(paths or DEFAULT_SOURCES)
        findings = json.loads((self.supplied_dir / "source_findings.json").read_text(encoding="utf-8-sig"))
        sections = json.loads((self.supplied_dir / "report_sections.json").read_text(encoding="utf-8-sig"))
        previous = self.store.current_catalog()
        catalog = catalog_mod.build_catalog(imports, findings, sections, self.rules,
                                            self.config["calculation_policy"], self.config["finding_classification"])
        manifest = {m["source_system"]: m for m in
                    json.loads((self.supplied_dir / "source_manifest.json").read_text(encoding="utf-8-sig"))}
        catalog["manifest_check"] = {system: {"manifest_sha256": manifest.get(system, {}).get("sha256"),
                                              "imported_sha256": source["sha256"],
                                              "matches_supplied_evidence_version":
                                                  manifest.get(system, {}).get("sha256") == source["sha256"]}
                                     for system, source in catalog["sources"].items()}
        version = self.store.save_catalog(catalog, self.config.hashes(), note)
        catalog = self.store.current_catalog()
        changes = self._diff_catalogs(previous, catalog) if previous else None
        stale = [d for d in self.decision_rows() if d["validity"] in ("STALE", "ORPHANED")]
        return {"catalog_version": version, "sources": catalog["sources"], "manifest_check": catalog["manifest_check"],
                "mapping_count": len(catalog["mappings"]), "changes": changes,
                "stale_or_orphaned_decisions": len(stale)}

    @staticmethod
    def _diff_catalogs(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
        before = {m["business_id"]: m["fingerprint"] for m in old["mappings"]}
        after = {m["business_id"]: m["fingerprint"] for m in new["mappings"]}
        return {"added": sorted(set(after) - set(before)), "removed": sorted(set(before) - set(after)),
                "changed": sorted(k for k in set(before) & set(after) if before[k] != after[k])}

    # ---- lookups ----------------------------------------------------------
    @property
    def catalog(self) -> dict[str, Any]:
        catalog = self.store.current_catalog()
        if catalog is None:
            raise RuntimeError("No catalog imported yet. Run: python -m nbs_control refresh")
        return catalog

    def mapping(self, business_id: str) -> dict[str, Any]:
        for item in self.catalog["mappings"]:
            if item["business_id"] == business_id:
                return item
        raise KeyError(business_id)

    def section(self, section_id: str) -> dict[str, Any]:
        for item in self.catalog["sections"]:
            if item["section_id"] == section_id:
                return item
        raise KeyError(section_id)

    def finding_item(self, item_id: str) -> dict[str, Any]:
        for item in self.catalog["findings_queue"]:
            if item["item_id"] == item_id:
                return item
        raise KeyError(item_id)

    # ---- decisions --------------------------------------------------------
    def _validate_spec(self, spec: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
        unknown = set(spec) - set(SPEC_KEYS)
        if unknown:
            raise DecisionError(f"Unknown specification keys: {sorted(unknown)}")
        policy = self.config["calculation_policy"]
        expression = spec.get("metric_expression")
        try:
            terms = parse_expression(expression or "")
        except ValueError as exc:
            raise DecisionError(f"metric_expression: {exc}") from exc
        for _, name in terms:
            if name not in policy["metrics"]:
                raise DecisionError(f"metric_expression references unknown metric {name}")
        if spec.get("amount_basis") not in policy["amount_bases"]:
            raise DecisionError("amount_basis must be one of " + ", ".join(policy["amount_bases"]))
        if spec.get("selectors") is None:
            raise DecisionError("A structured selector is required (see config/report_selectors.json fields)")
        try:
            validate_selector(spec["selectors"], self.config["report_selectors"]["fields"], require_approved=False)
        except SelectorError as exc:
            raise DecisionError(f"selectors: {exc}") from exc
        for key in ("effective_from", "effective_to"):
            if spec.get(key):
                try:
                    date.fromisoformat(spec[key])
                except ValueError as exc:
                    raise DecisionError(f"{key} must be YYYY-MM-DD") from exc
        if spec.get("effective_from") and spec.get("effective_to") and spec["effective_from"] > spec["effective_to"]:
            raise DecisionError("effective_from is after effective_to")
        targets = spec.get("nbs_target_business_ids") or []
        if item["source_system"] == "ETHIX":
            allowed = {c["business_id"] for c in item.get("nbs_row_candidates", [])}
            if any(t not in allowed for t in targets):
                raise DecisionError("nbs_target_business_ids must come from this row's full-path candidates")
        elif targets:
            raise DecisionError("nbs_target_business_ids applies only to Ethix rows")
        return {key: spec.get(key) for key in SPEC_KEYS if spec.get(key) not in (None, "", [])}

    def decide_mapping(self, business_id: str, action: str, *, actor: str, reason: str, approved_on: str | None = None,
                       approval_evidence: str | None = None, spec: dict[str, Any] | None = None,
                       origin: str = "UI") -> dict[str, Any]:
        item = self.mapping(business_id)
        payload: dict[str, Any] = {}
        if action == "APPROVE_PROPOSAL":
            proposal = item["proposal"]
            if proposal["status"] != "PROPOSED" or not proposal.get("metric_expression"):
                raise DecisionError("There is no complete proposal to approve; use APPROVE_OVERRIDE with a structured spec")
            merged = {"metric_expression": proposal["metric_expression"], "selectors": proposal.get("selectors"),
                      "amount_basis": proposal.get("amount_basis")}
            merged.update({k: v for k, v in (spec or {}).items() if v not in (None, "", [])})
            payload["spec"] = self._validate_spec(merged, item)
            payload["proposal_snapshot"] = proposal
        elif action == "APPROVE_OVERRIDE":
            payload["spec"] = self._validate_spec(spec or {}, item)
            payload["proposal_snapshot"] = item["proposal"]
        elif spec:
            payload["note_spec"] = spec
        return self.store.record("MAPPING", business_id, action, actor=actor, reason=reason,
                                 evidence_fingerprint=item["fingerprint"],
                                 catalog_version=self.catalog["catalog_version"], payload=payload,
                                 approved_on=approved_on, approval_evidence=approval_evidence, origin=origin)

    def decide_section(self, section_id: str, action: str, *, actor: str, reason: str, approved_on: str | None = None,
                       approval_evidence: str | None = None, block_keys: list[str] | None = None) -> dict[str, Any]:
        section = self.section(section_id)
        payload: dict[str, Any] = {}
        if action == "APPROVE_JOIN":
            candidates = {c["block_key"] for c in section["candidates"] if c["block_key"]}
            chosen = list(dict.fromkeys(block_keys or []))
            if not chosen:
                raise DecisionError("APPROVE_JOIN requires at least one NBS block")
            if any(key not in candidates for key in chosen):
                raise DecisionError("Chosen blocks must be among the section's candidate NBS blocks")
            payload["block_keys"] = chosen
        return self.store.record("SECTION", section_id, action, actor=actor, reason=reason,
                                 evidence_fingerprint=section["fingerprint"],
                                 catalog_version=self.catalog["catalog_version"], payload=payload,
                                 approved_on=approved_on, approval_evidence=approval_evidence)

    def decide_finding(self, item_id: str, action: str, *, actor: str, reason: str, approved_on: str | None = None,
                       approval_evidence: str | None = None) -> dict[str, Any]:
        item = self.finding_item(item_id)
        return self.store.record("FINDING", item_id, action, actor=actor, reason=reason,
                                 evidence_fingerprint=item["fingerprint"],
                                 catalog_version=self.catalog["catalog_version"],
                                 approved_on=approved_on, approval_evidence=approval_evidence)

    # ---- validity / effectiveness -----------------------------------------
    @staticmethod
    def validity(decision: dict[str, Any] | None, fingerprint: str | None) -> str:
        if decision is None:
            return "NONE"
        if fingerprint is None:
            return "ORPHANED"
        return "CURRENT" if decision["evidence_fingerprint"] == fingerprint else "STALE"

    def _context(self) -> dict[str, Any]:
        catalog = self.catalog
        sections = self.store.current_all("SECTION")
        findings = self.store.current_all("FINDING")
        block_section: dict[str, list[dict[str, Any]]] = {}
        for section in catalog["sections"]:
            for candidate in section["candidates"]:
                if candidate["block_key"]:
                    block_section.setdefault(candidate["block_key"], []).append(section)
        ethix_section = {s["ethix_block_key"]: s for s in catalog["sections"] if s["ethix_block_key"]}
        open_findings: dict[str, list[str]] = {}
        for entry in catalog["findings_queue"]:
            if not entry["blocking"] or not entry["business_id"]:
                continue
            decision = findings.get(entry["item_id"])
            ok = (decision is not None and decision["action"] in RESOLVED_FINDING_ACTIONS
                  and self.validity(decision, entry["fingerprint"]) == "CURRENT")
            if not ok:
                open_findings.setdefault(entry["business_id"], []).append(entry["finding_id"])
        return {"sections": sections, "block_section": block_section, "ethix_section": ethix_section,
                "open_findings": open_findings, "mappings": self.store.current_all("MAPPING")}

    def _section_ok(self, section: dict[str, Any], decisions: dict[str, Any], block_key: str | None) -> list[str]:
        decision = decisions.get(section["section_id"])
        if decision is None or decision["action"] != "APPROVE_JOIN":
            return [f"SECTION_JOIN_NOT_APPROVED:{section['identity']}"]
        if self.validity(decision, section["fingerprint"]) != "CURRENT":
            return [f"SECTION_DECISION_STALE:{section['identity']}"]
        if block_key and block_key not in decision["payload"].get("block_keys", []):
            return [f"BLOCK_NOT_IN_APPROVED_JOIN:{block_key}"]
        return []

    def evaluate(self, item: dict[str, Any], ctx: dict[str, Any] | None = None, as_of: str | None = None) -> dict[str, Any]:
        ctx = ctx or self._context()
        decision = ctx["mappings"].get(item["business_id"])
        validity = self.validity(decision, item["fingerprint"])
        reasons: list[str] = []
        if decision is None:
            state = "NO_DECISION"
            reasons.append("NO_OWNER_DECISION")
        elif validity == "STALE":
            state = "STALE"
            reasons.append("DECISION_STALE_SOURCE_EVIDENCE_CHANGED")
        elif decision["action"] in ("REJECT", "NOT_APPLICABLE"):
            state = decision["action"]
        elif decision["action"] in ("DEFER", "RECORD_REVIEW_NOTE"):
            state = "DEFERRED" if decision["action"] == "DEFER" else "REVIEW_NOTE_ONLY"
            reasons.append("NOT_AN_EXECUTABLE_DECISION")
        else:
            reasons += self._spec_reasons(item, decision["payload"]["spec"], ctx, as_of)
            state = "EFFECTIVE" if not reasons else "APPROVED_BLOCKED"
        return {"business_id": item["business_id"], "state": state, "validity": validity,
                "decision": decision, "reasons": reasons}

    def _spec_reasons(self, item: dict[str, Any], spec: dict[str, Any], ctx: dict[str, Any], as_of: str | None) -> list[str]:
        reasons: list[str] = []
        policy = self.config["calculation_policy"]
        selectors_cfg = self.config["report_selectors"]
        terms = parse_expression(spec["metric_expression"])
        for _, name in terms:
            status = metric_status(name, policy, self.rules)
            reasons += [f"METRIC_UNAVAILABLE:{r}" for r in status["reasons"]]
            metric = policy["metrics"].get(name)
            if metric and metric["amount_basis"] != spec["amount_basis"]:
                reasons.append(f"AMOUNT_BASIS_MISMATCH:{name}")
        if not policy["amount_bases"][spec["amount_basis"]].get("approved"):
            reasons.append(f"AMOUNT_BASIS_NOT_APPROVED:{spec['amount_basis']}")
        if spec["amount_basis"] == "CLOSING_STOCK" and not policy.get("ecb_adapter", {}).get("approved"):
            reasons.append("ECB_ADAPTER_POLICY_NOT_APPROVED")
        try:
            used = validate_selector(spec["selectors"], selectors_cfg["fields"], require_approved=False)
            for field in sorted(used):
                if selectors_cfg["fields"][field].get("status") != "APPROVED":
                    reasons.append(f"SELECTOR_FIELD_NOT_APPROVED:{field}")
        except SelectorError as exc:
            reasons.append(f"SELECTOR_INVALID:{exc}")
        uses_balance_groups = any(policy["metrics"].get(n, {}).get("kind") in ("BALANCE_GROUP", "COMPOSITE") for _, n in terms)
        if uses_balance_groups:
            population = selectors_cfg.get("populations", {}).get("LENDING_BASE", {})
            if population.get("status") != "APPROVED":
                reasons.append("LENDING_POPULATION_NOT_APPROVED")
            if catalog_mod._selector_may_include(spec["selectors"], self.rules["candidate_category"]):
                credit = self.rules["extra_approval"].get("CREDIT", {})
                if not credit.get("owner_approved"):
                    reasons.append("CLM_CREDIT_GROUP_NOT_APPROVED")
                if not self.config["balance_rules"].get("virtual_balances"):
                    reasons.append("CLM_EMBEDDING_IN_VIRTUAL_BALANCES_UNVERIFIED")
        as_of = as_of or date.today().isoformat()
        if spec.get("effective_from") and spec["effective_from"] > as_of:
            reasons.append("NOT_YET_EFFECTIVE")
        if spec.get("effective_to") and spec["effective_to"] < as_of:
            reasons.append("EXPIRED")
        if item["source_system"] == "ETHIX":
            section = ctx["ethix_section"].get(item["block_key"])
            if section is None:
                reasons.append("ETHIX_SECTION_UNKNOWN")
            else:
                reasons += self._section_ok(section, ctx["sections"], None)
            if not spec.get("nbs_target_business_ids"):
                reasons.append("ETHIX_ROW_JOIN_NOT_SELECTED")
        else:
            for section in ctx["block_section"].get(item["block_key"], []):
                if len(section["candidates"]) > 1:
                    reasons += self._section_ok(section, ctx["sections"], item["block_key"])
        for finding in ctx["open_findings"].get(item["business_id"], []):
            reasons.append(f"OPEN_FINDING:{finding}")
        return list(dict.fromkeys(reasons))

    # ---- views ------------------------------------------------------------
    def proposed_view(self) -> list[dict[str, Any]]:
        return [item for item in self.catalog["mappings"] if item["proposal"]["status"] == "PROPOSED"]

    def decision_rows(self) -> list[dict[str, Any]]:
        catalog = self.store.current_catalog()
        if catalog is None:
            return []
        fingerprints = {
            "MAPPING": {m["business_id"]: m["fingerprint"] for m in catalog["mappings"]},
            "SECTION": {s["section_id"]: s["fingerprint"] for s in catalog["sections"]},
            "FINDING": {f["item_id"]: f["fingerprint"] for f in catalog["findings_queue"]},
        }
        rows = []
        for kind in ("MAPPING", "SECTION", "FINDING"):
            for subject, decision in self.store.current_all(kind).items():
                rows.append({**decision, "validity": self.validity(decision, fingerprints[kind].get(subject))})
        return sorted(rows, key=lambda r: r["event_id"], reverse=True)

    def evaluations(self, as_of: str | None = None) -> list[dict[str, Any]]:
        ctx = self._context()
        return [{**self.evaluate(item, ctx, as_of), "item": item} for item in self.catalog["mappings"]]

    def effective_view(self, as_of: str | None = None) -> list[dict[str, Any]]:
        return [e for e in self.evaluations(as_of) if e["state"] == "EFFECTIVE"]

    def effective_compiled(self, as_of: str | None = None) -> list[dict[str, Any]]:
        fields = self.config["report_selectors"]["fields"]
        result = []
        for entry in self.effective_view(as_of):
            spec = entry["decision"]["payload"]["spec"]
            compile_selector(spec["selectors"], fields, require_approved=True)
            result.append({"business_id": entry["business_id"], "effective_spec": spec, "item": entry["item"]})
        return result

    def unresolved_view(self, as_of: str | None = None) -> dict[str, Any]:
        evaluations = self.evaluations(as_of)
        mappings = [e for e in evaluations
                    if (e["item"]["kind"] == "RULE" and e["state"] not in ("EFFECTIVE", "REJECT", "NOT_APPLICABLE"))
                    or (e["item"]["kind"] != "RULE" and e["state"] in ("STALE", "APPROVED_BLOCKED"))]
        sections_dec = self.store.current_all("SECTION")
        sections = []
        for section in self.catalog["sections"]:
            decision = sections_dec.get(section["section_id"])
            validity = self.validity(decision, section["fingerprint"])
            if decision is None or validity != "CURRENT" or decision["action"] == "DEFER":
                sections.append({"section": section, "decision": decision, "validity": validity})
        findings_dec = self.store.current_all("FINDING")
        findings = []
        for entry in self.catalog["findings_queue"]:
            decision = findings_dec.get(entry["item_id"])
            validity = self.validity(decision, entry["fingerprint"])
            if decision is None or validity != "CURRENT" or decision["action"] not in RESOLVED_FINDING_ACTIONS:
                findings.append({"entry": entry, "decision": decision, "validity": validity})
        return {"mappings": mappings, "sections": sections, "findings": findings, "global": self.global_open_items()}

    def global_open_items(self) -> list[dict[str, str]]:
        """Configuration-level inputs and approvals that block or limit effective mappings."""
        items: list[dict[str, str]] = []
        policy = self.config["calculation_policy"]
        selectors = self.config["report_selectors"]
        rules_doc = self.config["balance_rules"]
        for name, metric in policy["metrics"].items():
            status = metric_status(name, policy, self.rules)
            if not status["available"]:
                items.append({"area": "Metric", "item": name, "detail": "; ".join(status["reasons"]) + f" - {metric.get('note', '')}"})
        for code, approval in self.rules["extra_approval"].items():
            if not approval["owner_approved"]:
                items.append({"area": "CLM", "item": f"{code} group assignment",
                              "detail": f"Proposed {self.rules['extra_membership'][code]}; owner approval required in config/balance_rules.json"})
        if not rules_doc["clm"].get("detector_field"):
            items.append({"area": "CLM", "item": "CLM indicator", "detail": "No positive CLM indicator field configured; CLM requires an explicit verified link or indicator"})
        if rules_doc.get("valid_balance_types") is None:
            items.append({"area": "Balances", "item": "Local AC.BALANCE.TYPE catalogue", "detail": "Not supplied; identifiers are not validated locally"})
        if rules_doc.get("virtual_balances") is None:
            items.append({"area": "Balances", "item": "Virtual balance composition", "detail": "Not supplied; aggregate-plus-component overlap and CLM embedding cannot be verified"})
        for basis, spec in policy["amount_bases"].items():
            if not spec.get("approved"):
                items.append({"area": "Calculation", "item": f"Amount basis {basis}", "detail": spec.get("description", "")})
        if not policy["ecb_adapter"].get("approved"):
            items.append({"area": "Calculation", "item": "ECB adapter", "detail": policy["ecb_adapter"].get("field_source", "")})
        if policy["ecb_adapter"].get("sparse_zero_convention") is None:
            items.append({"area": "Calculation", "item": "Sparse-zero convention", "detail": "None approved: every required balance must be supplied explicitly"})
        for key in ("maturity", "credit_quality", "currency"):
            if not policy.get(key, {}).get("approved"):
                items.append({"area": "Calculation", "item": f"{key} policy", "detail": policy.get(key, {}).get("note", "Requires owner approval")})
        for field, spec in selectors["fields"].items():
            if spec["system"] == "T24" and spec.get("status") != "APPROVED":
                items.append({"area": "Selector field", "item": field, "detail": spec.get("source", "")})
        for entry in selectors.get("crosswalk", []):
            if entry.get("status") != "APPROVED":
                items.append({"area": "Crosswalk", "item": entry["id"], "detail": entry.get("evidence", "")})
        for entry in selectors.get("contradictions", []):
            if entry.get("status") != "RESOLVED":
                items.append({"area": "Contradiction", "item": entry["id"], "detail": entry["description"]})
        for name, population in selectors.get("populations", {}).items():
            if population.get("status") != "APPROVED":
                items.append({"area": "Population", "item": name, "detail": population.get("note", "")})
        return items

    def summary(self) -> dict[str, Any]:
        catalog = self.catalog
        evaluations = self.evaluations()
        states: dict[str, int] = {}
        for e in evaluations:
            states[e["state"]] = states.get(e["state"], 0) + 1
        return {
            "catalog_version": catalog["catalog_version"],
            "sources": catalog["sources"],
            "manifest_check": catalog.get("manifest_check"),
            "populated_rows": len(catalog["mappings"]),
            "by_system": {s: sum(1 for m in catalog["mappings"] if m["source_system"] == s) for s in ("T24", "ETHIX")},
            "rule_rows": sum(1 for m in catalog["mappings"] if m["kind"] == "RULE"),
            "proposed": len(self.proposed_view()),
            "states": states,
            "sections": len(catalog["sections"]),
            "section_problems": sum(1 for s in catalog["sections"] if s["problems"]),
            "finding_items": len(catalog["findings_queue"]),
            "config_hashes": self.config.hashes(),
            "global_open_items": len(self.global_open_items()),
        }
