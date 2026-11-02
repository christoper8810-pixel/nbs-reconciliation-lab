"""Command-line entry point: python -m nbs_control <command>."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import DEFAULT_SOURCES, EXPORT_DIR, PROJECT_ROOT
from .config import ConfigError, parse_json


def _service(args):
    from .service import ControlService
    return ControlService(data_dir=args.data_dir) if args.data_dir else ControlService()


def _paths(args) -> dict[str, Path]:
    return {"T24": Path(args.t24 or DEFAULT_SOURCES["T24"]), "ETHIX": Path(args.ethix or DEFAULT_SOURCES["ETHIX"])}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nbs_control", description="NBS mapping control (review only)")
    parser.add_argument("--data-dir", help="State directory (default ./data)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("refresh", help="Re-import originals and rebuild the catalog")
    p.add_argument("--t24"); p.add_argument("--ethix")
    p.add_argument("--from-supplied-inventory", action="store_true",
                   help="Use the read-only source_inventory.json when originals are unavailable")
    p.add_argument("--note", default="")

    p = sub.add_parser("parity", help="Compare a fresh import with the supplied inventory")
    p.add_argument("--t24"); p.add_argument("--ethix")

    sub.add_parser("summary", help="Catalog and decision summary")

    for name in ("decide-mapping", "decide-section", "decide-finding"):
        p = sub.add_parser(name)
        p.add_argument("subject_id"); p.add_argument("action")
        p.add_argument("--actor", required=True); p.add_argument("--reason", required=True)
        p.add_argument("--approved-on"); p.add_argument("--evidence")
        if name == "decide-mapping":
            p.add_argument("--spec", help="JSON object or @file.json with the structured specification")
        if name == "decide-section":
            p.add_argument("--blocks", nargs="*", default=[])

    p = sub.add_parser("rollback")
    p.add_argument("kind", choices=("MAPPING", "SECTION", "FINDING")); p.add_argument("subject_id")
    p.add_argument("version", type=int); p.add_argument("--actor", required=True); p.add_argument("--reason", required=True)

    p = sub.add_parser("export", help="Write the three exports and the owner review workbook")
    p.add_argument("--dir", default=str(EXPORT_DIR))

    p = sub.add_parser("import-decisions", help="Apply decisions from an edited owner review workbook")
    p.add_argument("workbook"); p.add_argument("--actor")

    p = sub.add_parser("import-legacy-review", help="Record starter review-workbook decisions as review notes")
    p.add_argument("workbook")

    p = sub.add_parser("run-ecb", help="Review signed balances from an ECB JSON export")
    p.add_argument("--input", required=True); p.add_argument("--output", required=True)

    p = sub.add_parser("serve", help="Start the local owner review interface")
    p.add_argument("--port", type=int, default=8765)

    p = sub.add_parser('generate-reports', help='Generate NBS reports and compare with the supplied live Ethix report')
    p.add_argument('--database', default=str(PROJECT_ROOT/'data/bank_20260930.sqlite'))
    p.add_argument('--template', default=str(PROJECT_ROOT/'data/bank_sources/NBS01 Sep 2026 English.xlsx'))
    p.add_argument('--dir',default=str(EXPORT_DIR))

    p = sub.add_parser('rebuild-setup', help='Import category events, BO reference and live reference into the rebuild store')
    p.add_argument('--categ', action='append', help='Category workbook (repeatable; identical copies load once)')
    p.add_argument('--bo'); p.add_argument('--live')
    p.add_argument('--qcb', action='append', help='QCB NBS validation-rule workbook (repeatable)')
    p = sub.add_parser('build-bank-db', help='Build the read-only account database from the ECB, loan, deposit and trial-balance workbooks')
    p.add_argument('--ecb', required=True); p.add_argument('--loan', required=True); p.add_argument('--deposit', required=True); p.add_argument('--tb', required=True)
    p.add_argument('--out', default=str(PROJECT_ROOT/'data'/'bank_20260930.sqlite'))
    sub.add_parser('rebuild-enhance', help='Propose unreviewed drafts from the QCB code structure and validation rules')
    p = sub.add_parser('rebuild-export-mapping', help='Write the stakeholder mapping specification (Excel, JSON, CSV)')
    p.add_argument('--run', help='Run ID for figures (default: latest)'); p.add_argument('--out')
    sub.add_parser('rebuild-gl-evidence', help='Measure how much balance any GL-only mapping must misplace')
    p = sub.add_parser('rebuild-run', help='Generate a versioned rebuild run with comparisons, controls and Excel')
    p.add_argument('--report-date', default='2026-09-30'); p.add_argument('--label', default='')
    p.add_argument('--no-excel', action='store_true')

    args = parser.parse_args(argv)
    try:
        if args.command == 'rebuild-setup':
            from .rebuild_run import setup
            print(json.dumps(setup(PROJECT_ROOT, args.categ, args.bo, args.live, qcb_paths=args.qcb), indent=2, default=str))
            return 0
        if args.command == 'build-bank-db':
            from .bank_data import build_database
            m = build_database(args.ecb, {'LOAN': args.loan, 'DEPOSIT': args.deposit, 'TB': args.tb}, args.out)
            print(json.dumps({k: {'rows': v.get('rows'), 'sha256': v.get('sha256')} for k, v in m.items() if isinstance(v, dict) and 'rows' in v}, indent=2))
            return 0
        if args.command == 'rebuild-gl-evidence':
            from .rebuild_run import gl_evidence_file
            print(json.dumps(gl_evidence_file(PROJECT_ROOT)['summary'], indent=2))
            return 0
        if args.command == 'rebuild-export-mapping':
            from .mapping_export import export
            print(json.dumps(export(PROJECT_ROOT, args.run, args.out), indent=2))
            return 0
        if args.command == 'rebuild-enhance':
            from .rebuild_run import enhance_mappings
            print(json.dumps(enhance_mappings(PROJECT_ROOT), indent=2))
            return 0
        if args.command == 'rebuild-run':
            from .rebuild_run import run
            m = run(PROJECT_ROOT, args.report_date, label=args.label, export_excel=not args.no_excel)
            print(json.dumps({k: m[k] for k in ('run_id', 'statuses', 'summary', 'category_reporting_basis', 'excel') if k in m}, indent=2, default=str))
            return 0
        if args.command == "parity":
            from . import importer
            imported = importer.import_sources(_paths(args))
            result = importer.compare_with_supplied(imported, importer.load_supplied_inventory(PROJECT_ROOT / "source_inventory.json"))
            print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in result.items()}, indent=2))
            ok = not result["only_in_fresh"] and not result["only_in_supplied"] and not result["value_differences"]
            return 0 if ok and all(result["hash_match"].values()) else 2
        if args.command == "serve":
            from .web import create_app
            app = create_app(_service(args))
            print(f"Owner review interface: http://127.0.0.1:{args.port}  (local only, Ctrl+C to stop)")
            app.run(host="127.0.0.1", port=args.port, debug=False)
            return 0
        service = _service(args)
        if args.command=='generate-reports':
            from .generation import initialize_rules,generate
            config=service.config_dir/'generation_rules.json'
            initialize_rules(service,args.template,config)
            result=generate(args.database,args.template,config,service.config['balance_rules'],args.dir)
            print(json.dumps(result['summary'],indent=2))
            return 0
        if args.command == "refresh":
            result = service.refresh(None if args.from_supplied_inventory else _paths(args),
                                     use_supplied_inventory=args.from_supplied_inventory, note=args.note)
            if result["changes"]:
                result["changes"] = {k: len(v) for k, v in result["changes"].items()}
            print(json.dumps(result, indent=2))
            return 0
        if args.command == "summary":
            print(json.dumps(service.summary(), indent=2))
            return 0
        if args.command == "decide-mapping":
            spec = None
            if args.spec:
                text = Path(args.spec[1:]).read_text(encoding="utf-8") if args.spec.startswith("@") else args.spec
                spec = parse_json(text)
            result = service.decide_mapping(args.subject_id, args.action, actor=args.actor, reason=args.reason,
                                            approved_on=args.approved_on, approval_evidence=args.evidence,
                                            spec=spec, origin="CLI")
            evaluation = service.evaluate(service.mapping(args.subject_id))
            print(json.dumps({"decision": result, "state": evaluation["state"], "reasons": evaluation["reasons"]}, indent=2))
            return 0
        if args.command == "decide-section":
            print(json.dumps(service.decide_section(args.subject_id, args.action, actor=args.actor, reason=args.reason,
                                                    approved_on=args.approved_on, approval_evidence=args.evidence,
                                                    block_keys=args.blocks), indent=2))
            return 0
        if args.command == "decide-finding":
            print(json.dumps(service.decide_finding(args.subject_id, args.action, actor=args.actor, reason=args.reason,
                                                    approved_on=args.approved_on, approval_evidence=args.evidence), indent=2))
            return 0
        if args.command == "rollback":
            print(json.dumps(service.store.rollback(args.kind, args.subject_id, args.version, args.actor, args.reason), indent=2))
            return 0
        if args.command == "export":
            from .exports import export_all
            print(json.dumps(export_all(service, Path(args.dir)), indent=2))
            return 0
        if args.command == "import-decisions":
            from .exports import import_owner_workbook
            result = import_owner_workbook(service, Path(args.workbook), args.actor)
            print(json.dumps(result, indent=2))
            return 0 if not result["errors"] else 2
        if args.command == "import-legacy-review":
            from .exports import import_legacy_review_workbook
            print(json.dumps(import_legacy_review_workbook(service, Path(args.workbook)), indent=2))
            return 0
        if args.command == "run-ecb":
            from .ecb_adapter import run_review
            payload = parse_json(Path(args.input).read_text(encoding="utf-8-sig"))
            result = run_review(payload, service.rules, service.config["balance_rules"],
                                service.config["calculation_policy"], service.config["report_selectors"])
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({"output": args.output, "production_ready": False,
                              "complete": result["complete_for_supplied_records_and_required_types"],
                              "exceptions": len(result["adapter"]["exceptions"])}, indent=2))
            return 0 if result["complete_for_supplied_records_and_required_types"] else 2
    except (ConfigError, ValueError, KeyError, FileNotFoundError, RuntimeError) as exc:
        print(json.dumps({"status": "ERROR", "detail": str(exc)}), file=sys.stderr)
        return 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
