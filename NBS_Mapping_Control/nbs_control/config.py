"""Versioned JSON configuration with validation and saved history.

Every save validates the whole document first, keeps the previous file in
config/history, and records a content hash so decisions and runs can cite the
exact configuration they used.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import mapping_engine

from . import CONFIG_DIR

CONFIG_NAMES = ("balance_rules", "calculation_policy", "report_selectors", "finding_classification")


class ConfigError(ValueError):
    """A configuration document is invalid."""


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ConfigError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json(text: str) -> Any:
    return json.loads(text, object_pairs_hook=_strict_object)


def content_hash(document: Any) -> str:
    canonical = json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _check_approval(item: dict[str, Any], label: str) -> None:
    if item.get("status") == "APPROVED":
        for key in ("approved_by", "approved_on"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ConfigError(f"{label} is APPROVED without {key}")
        try:
            datetime.strptime(item["approved_on"], "%Y-%m-%d")
        except ValueError as exc:
            raise ConfigError(f"{label} approved_on must be YYYY-MM-DD") from exc


def validate_balance_rules(doc: Any) -> None:
    try:
        mapping_engine.validate_rules(doc)
    except mapping_engine.RuleError as exc:
        raise ConfigError(str(exc)) from exc
    virtual = doc.get("virtual_balances")
    if virtual is not None:
        if not isinstance(virtual, dict) or not virtual:
            raise ConfigError("virtual_balances must be null or a nonempty object")
        for code, parts in virtual.items():
            if not isinstance(parts, list) or not parts or not all(isinstance(p, str) and p.strip() for p in parts):
                raise ConfigError(f"virtual balance {code} needs a nonempty component list")
    for key in ("true_values", "false_values"):
        values = doc.get("clm", {}).get(key, [])
        if not isinstance(values, list):
            raise ConfigError(f"clm.{key} must be a list")
    clm = doc.get("clm", {})
    overlap = set(map(str, clm.get("true_values", []))) & set(map(str, clm.get("false_values", [])))
    if overlap:
        raise ConfigError(f"CLM indicator values cannot be both true and false: {sorted(overlap)}")


def validate_calculation_policy(doc: Any) -> None:
    from .report_calc import validate_maturity_buckets
    from .selectors import parse_expression

    if not isinstance(doc, dict) or not isinstance(doc.get("metrics"), dict):
        raise ConfigError("calculation_policy.metrics must be an object")
    bases = doc.get("amount_bases")
    if not isinstance(bases, dict) or not bases:
        raise ConfigError("calculation_policy.amount_bases must be a nonempty object")
    for name, metric in doc["metrics"].items():
        if not isinstance(metric, dict) or metric.get("kind") not in ("BALANCE_GROUP", "COMPOSITE", "UNDEFINED"):
            raise ConfigError(f"metric {name} needs kind BALANCE_GROUP, COMPOSITE or UNDEFINED")
        if metric.get("amount_basis") not in bases:
            raise ConfigError(f"metric {name} uses unknown amount_basis {metric.get('amount_basis')}")
        if metric["kind"] == "BALANCE_GROUP" and metric.get("group") not in mapping_engine.GROUPS:
            raise ConfigError(f"metric {name} references unknown balance group")
        if metric["kind"] == "COMPOSITE":
            try:
                terms = parse_expression(metric.get("expression", ""))
            except ValueError as exc:
                raise ConfigError(f"metric {name}: {exc}") from exc
            for _, ref in terms:
                if ref not in doc["metrics"] or ref == name:
                    raise ConfigError(f"metric {name} references unknown metric {ref}")
                if doc["metrics"][ref].get("amount_basis") != metric["amount_basis"]:
                    raise ConfigError(f"metric {name} mixes amount bases")
    adapter = doc.get("ecb_adapter", {})
    if adapter.get("mode") not in adapter.get("allowed_modes", []):
        raise ConfigError("ecb_adapter.mode must be one of allowed_modes")
    if adapter.get("date_basis") not in adapter.get("allowed_date_bases", []):
        raise ConfigError("ecb_adapter.date_basis must be one of allowed_date_bases")
    if adapter.get("movement_sign_convention") != "AS_SUPPLIED_SIGNED":
        raise ConfigError("Only AS_SUPPLIED_SIGNED movements are supported; signs are never invented")
    sparse = adapter.get("sparse_zero_convention")
    if sparse is not None:
        if not isinstance(sparse, dict) or sparse.get("applies_to") != "BASE_TYPES":
            raise ConfigError("sparse_zero_convention must be null or {approved_by, approved_on, applies_to: BASE_TYPES}")
        _check_approval({**sparse, "status": "APPROVED"}, "sparse_zero_convention")
    problems = validate_maturity_buckets(doc.get("maturity", {}).get("buckets", []))
    if problems:
        raise ConfigError("maturity buckets: " + "; ".join(problems))


def validate_report_selectors(doc: Any) -> None:
    if not isinstance(doc, dict) or not isinstance(doc.get("fields"), dict):
        raise ConfigError("report_selectors.fields must be an object")
    for name, field in doc["fields"].items():
        if not isinstance(field, dict) or field.get("system") not in ("T24", "ETHIX"):
            raise ConfigError(f"field {name} needs system T24 or ETHIX")
        if field.get("system") == "ETHIX" and field.get("status") == "APPROVED":
            raise ConfigError(f"Legacy field {name} cannot be approved for executable T24 selectors")
        _check_approval(field, f"field {name}")
    from .selectors import validate_selector

    for name, population in doc.get("populations", {}).items():
        _check_approval(population, f"population {name}")
        validate_selector(population.get("selector"), doc["fields"], require_approved=False)


def validate_finding_classification(doc: Any) -> None:
    if not isinstance(doc, dict) or not isinstance(doc.get("findings"), dict):
        raise ConfigError("finding_classification.findings must be an object")
    kinds = doc.get("kinds", {})
    for finding, kind in doc["findings"].items():
        if kind not in kinds:
            raise ConfigError(f"finding {finding} uses unknown kind {kind}")


VALIDATORS = {
    "balance_rules": validate_balance_rules,
    "calculation_policy": validate_calculation_policy,
    "report_selectors": validate_report_selectors,
    "finding_classification": validate_finding_classification,
}


class ConfigSet:
    """All configuration documents loaded from one directory."""

    def __init__(self, directory: Path = CONFIG_DIR):
        self.directory = Path(directory)
        self.docs: dict[str, Any] = {}
        for name in CONFIG_NAMES:
            self.docs[name] = load_config(name, self.directory)

    def __getitem__(self, name: str) -> Any:
        return self.docs[name]

    @property
    def engine_rules(self) -> dict[str, Any]:
        return mapping_engine.validate_rules(self.docs["balance_rules"])

    def hashes(self) -> dict[str, str]:
        return {name: content_hash(doc) for name, doc in self.docs.items()}


def config_path(name: str, directory: Path = CONFIG_DIR) -> Path:
    if name not in CONFIG_NAMES:
        raise ConfigError(f"Unknown configuration: {name}")
    return Path(directory) / f"{name}.json"


def load_config(name: str, directory: Path = CONFIG_DIR) -> Any:
    path = config_path(name, directory)
    doc = parse_json(path.read_text(encoding="utf-8-sig"))
    VALIDATORS[name](doc)
    return doc


def save_config(name: str, text: str, actor: str, reason: str, directory: Path = CONFIG_DIR) -> dict[str, Any]:
    """Validate and save a configuration document, preserving the previous version."""
    if not actor.strip() or not reason.strip():
        raise ConfigError("Configuration changes require an actor and a reason")
    doc = parse_json(text)
    VALIDATORS[name](doc)
    path = config_path(name, directory)
    history = Path(directory) / "history"
    history.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    previous_hash = None
    if path.exists():
        previous = path.read_text(encoding="utf-8-sig")
        previous_hash = content_hash(parse_json(previous))
        (history / f"{name}.{stamp}.json").write_text(previous, encoding="utf-8")
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    entry = {"config": name, "at": stamp, "actor": actor.strip(), "reason": reason.strip(),
             "previous_hash": previous_hash, "new_hash": content_hash(doc)}
    with (history / "changes.jsonl").open("a", encoding="utf-8") as log:
        log.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def config_history(directory: Path = CONFIG_DIR) -> list[dict[str, Any]]:
    log = Path(directory) / "history" / "changes.jsonl"
    if not log.exists():
        return []
    return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip()]


def restore_config(name: str, stamp: str, actor: str, reason: str, directory: Path = CONFIG_DIR) -> dict[str, Any]:
    """Roll back by saving a historical copy as a new version (history is never rewritten)."""
    if not stamp.replace("T", "").replace("Z", "").isdigit():
        raise ConfigError("Invalid history stamp")
    source = Path(directory) / "history" / f"{name}.{stamp}.json"
    if not source.exists():
        raise ConfigError(f"No saved version {stamp} for {name}")
    return save_config(name, source.read_text(encoding="utf-8"), actor, f"Rollback to {stamp}: {reason}", directory)
