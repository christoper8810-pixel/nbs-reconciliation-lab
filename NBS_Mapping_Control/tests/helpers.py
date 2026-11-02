"""Shared fixtures: isolated config/data/supplied directories and synthetic ECB payloads."""

from __future__ import annotations

import copy
import json
import shutil
import tempfile
from pathlib import Path

import mapping_engine

ROOT = Path(__file__).resolve().parent.parent
SUPPLIED_FILES = ("source_inventory.json", "source_manifest.json", "source_findings.json", "report_sections.json")
BASE = ["CURACCOUNT", "PREACCOUNT", "GRCACCOUNT", "DELACCOUNT", "NABACCOUNT", "DUEACCOUNT", "DELDEFERREDPFT",
        "GRCDEFERREDPFT", "NABDEFERREDPFT", "DUEDEFERREDPFT", "RECDEFERREDPFT", "PREDEFERREDPFT", "ACCPRINCIPALPFT",
        "RECPRINCIPALPFT", "GRCPRINCIPALPFT", "DELPRINCIPALPFT", "PREPRINCIPALPFT", "DEFERREDPFT", "ACCDEFERREDPFT"]

_TEMPLATE: Path | None = None


def config_docs() -> dict:
    return {name: json.loads((ROOT / "config" / f"{name}.json").read_text(encoding="utf-8"))
            for name in ("balance_rules", "calculation_policy", "report_selectors", "finding_classification")}


def template_environment() -> Path:
    """Build one catalog from the supplied inventory, reused (copied) by every service test."""
    global _TEMPLATE
    if _TEMPLATE is None:
        from nbs_control.service import ControlService
        _TEMPLATE = Path(tempfile.mkdtemp(prefix="nbs-template-"))
        shutil.copytree(ROOT / "config", _TEMPLATE / "config", ignore=shutil.ignore_patterns("history"))
        (_TEMPLATE / "supplied").mkdir()
        for name in SUPPLIED_FILES:
            shutil.copy(ROOT / name, _TEMPLATE / "supplied" / name)
        service = ControlService(_TEMPLATE / "config", _TEMPLATE / "data", _TEMPLATE / "supplied")
        service.refresh(use_supplied_inventory=True, note="test template")
    return _TEMPLATE


class Environment:
    def __init__(self):
        self.root = Path(tempfile.mkdtemp(prefix="nbs-test-"))
        shutil.copytree(template_environment(), self.root, dirs_exist_ok=True)

    def service(self):
        from nbs_control.service import ControlService
        return ControlService(self.root / "config", self.root / "data", self.root / "supplied")

    def edit_config(self, name: str, mutate) -> None:
        path = self.root / "config" / f"{name}.json"
        doc = json.loads(path.read_text(encoding="utf-8"))
        mutate(doc)
        path.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    def cleanup(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)


def ecb_record(record_id, contract, category, types=None, opening=None, credit=None, debit=None, currency="QAR",
               **extra):
    types = list(BASE) if types is None else types
    zeros = ["0"] * len(types)
    return {"record_id": record_id, "company": "CO", "source_system": "T24", "contract_id": contract,
            "currency": currency, "snapshot_as_of": "2026-10-06", "date_basis": "BOOK", "category": category,
            "CURR.ASSET.TYPE": types, "OPEN.BALANCE": opening or list(zeros), "CREDIT.MVMT": credit or list(zeros),
            "DEBIT.MVMT": debit or list(zeros), **extra}


def link(parent="MUR-1", child="CLS-1", link_id="L1", **overrides):
    value = {"link_id": link_id, "company": "CO", "source_system": "T24", "as_of": "2026-10-06", "currency": "QAR",
             "parent_contract_id": parent, "parent_category": "3713", "child_contract_id": child,
             "child_category": "6050", "child_product": "CLS", "verified": True, "evidence": "test relationship"}
    value.update(overrides)
    return value


def adapter_config(credit_approved=False, virtual=None, **policy_changes):
    docs = config_docs()
    rules_doc = docs["balance_rules"]
    if credit_approved:
        for extra in rules_doc["clm"]["extra_balances"]:
            if extra["balance_type"] == "CREDIT":
                extra.update(owner_approved=True, approved_by="Test owner", approved_on="2026-10-14")
    rules_doc["virtual_balances"] = virtual
    policy = docs["calculation_policy"]
    policy["ecb_adapter"].update(policy_changes)
    return mapping_engine.validate_rules(rules_doc), rules_doc, policy, docs["report_selectors"]


def deep(value):
    return copy.deepcopy(value)
