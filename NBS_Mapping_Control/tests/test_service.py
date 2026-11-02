"""Catalog, owner decisions, effectiveness, refresh invalidation, rollback and exports."""

import json
import unittest
from collections import Counter
from pathlib import Path

import openpyxl

from nbs_control.config import ConfigError, config_history, restore_config, save_config
from nbs_control.exports import (DECISION_COLUMNS, export_all, export_owner_workbook, import_legacy_review_workbook,
                                 import_owner_workbook)
from nbs_control.store import DecisionError

from tests.helpers import ROOT, Environment

APPROVAL = {"actor": "Report Owner", "reason": "Reviewed against Ethix meaning", "approved_on": "2026-10-14",
            "approval_evidence": "Owner review minute 2026-10-14"}


def find(service, sheet, row, system="T24"):
    return next(m for m in service.catalog["mappings"]
                if m["source_system"] == system and m["sheet"] == sheet and m["source_row"] == row)


class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.env = Environment()
        self.service = self.env.service()

    def tearDown(self):
        self.env.cleanup()


class CatalogTests(ServiceTestCase):
    def test_coverage_inventory_and_identities(self):
        catalog = self.service.catalog
        mappings = catalog["mappings"]
        self.assertEqual(len(mappings), 4013)
        self.assertEqual(Counter(m["source_system"] for m in mappings), {"T24": 2149, "ETHIX": 1864})
        supplied = json.loads((ROOT / "source_inventory.json").read_text(encoding="utf-8-sig"))
        self.assertEqual({m["source_id"] for m in mappings}, {r["source_id"] for r in supplied})
        self.assertEqual(len({m["business_id"] for m in mappings}), 4013)
        self.assertTrue(all(m["business_id"].startswith("BM-") and m["source_id"] != m["business_id"] for m in mappings))
        self.assertTrue(all(m["source_hash"] in (catalog["sources"]["T24"]["sha256"], catalog["sources"]["ETHIX"]["sha256"])
                            for m in mappings))
        self.assertTrue(all(c["coord"] for m in mappings for c in m["cells"]))
        self.assertEqual(sum(1 for m in mappings for c in m["cells"] if c.get("note")), 58)
        self.assertEqual(self.service.summary()["states"], {"NO_DECISION": 4013})

    def test_section_alignment_missing_table38_and_repeated_blocks(self):
        sections = {s["identity"]: s for s in self.service.catalog["sections"]}
        self.assertEqual(len(sections), 49)
        self.assertEqual(sections["T38|R303"]["problems"], ["MISSING_NBS_MAPPING"])
        detail = [s for s in self.service.catalog["sections"] if s["table_number"] is not None]
        self.assertEqual(sum(1 for s in detail if s["candidates"]), 43)
        table6 = sections["T6|R104"]
        self.assertEqual(table6["problems"], ["BLOCK_IDENTITY_REQUIRED"])
        self.assertEqual([c["block_key"] for c in table6["candidates"]], ["T24|TABLE 6|B1", "T24|TABLE 6|B2"])
        b1 = find(self.service, "Table 6", 8)
        b2 = next(m for m in self.service.catalog["mappings"] if m["sheet"] == "Table 6"
                  and m["block_key"] == "T24|TABLE 6|B2" and m["path_key"].endswith(b1["path_key"].split(" > ")[-1]))
        self.assertNotEqual(b1["business_id"], b2["business_id"])  # same labels, different block identity

    def test_ethix_rows_join_only_on_full_hierarchy_path(self):
        ethix = find(self.service, "All Reports By Report ID_Templa", 33, "ETHIX")
        targets = ethix["nbs_row_candidates"]
        self.assertEqual({t["block_key"] for t in targets}, {"T24|ASSET - 100|B1", "T24|ASSET - 100|B2"})
        for target in targets:
            nbs = self.service.mapping(target["business_id"])
            self.assertEqual(nbs["path_key"], ethix["path_key"])

    def test_loan_proposals_follow_owner_dictionary(self):
        t8 = find(self.service, "Table 8", 20)["proposal"]
        self.assertEqual(t8["metric_expression"], "OUTSTANDING")
        self.assertEqual(t8["token_diff"]["unknown"], ["PDOACCOUNT"])
        self.assertEqual(len(t8["token_diff"]["missing_from_legacy"]), 6)
        others = find(self.service, "Table 8", 27)["proposal"]
        self.assertTrue(any("3713" in note for note in others["notes"]))
        self.assertEqual(others["selectors"]["all"][1]["values"], ["3701", "3717", "3704", "3702", "3706"])  # unchanged
        row26 = find(self.service, "Table 11", 26)["proposal"]
        self.assertEqual(row26["metric_expression"], "UNEARNED_PROFIT")
        self.assertEqual(row26["token_diff"]["unknown"], ["PDODEFERREDPFT"])
        row25 = find(self.service, "Table 11", 25)["proposal"]
        self.assertEqual(row25["metric_expression"], "SUSPENSE_SP")
        carrying = [m for m in self.service.catalog["mappings"]
                    if m["proposal"]["metric_expression"] == "ETHIX_LOAN_CARRYING_AMOUNT"]
        self.assertEqual(sorted(m["source_row"] for m in carrying), [33, 35, 37, 40, 41])
        cells = [c for m in carrying for c in m["cells"] if "loan_fees_qar" in str(c["value"]).lower()]
        self.assertEqual(len(cells), 7)
        self.assertTrue(all(any("LOAN_FEES" in d for d in m["proposal"]["dependencies"]) for m in carrying))

    def test_formula_and_maturity_corrections_are_cell_level(self):
        row5 = find(self.service, "Table 11", 5)["proposal"]["formula_corrections"]
        proposed = {c["coord"]: c["proposed"] for c in row5}
        self.assertEqual(proposed, {"G5": "=C5+E5", "N5": "=H5+J5+L5", "O5": "=I5+K5+M5", "P5": "=F5+N5", "Q5": "=G5+O5"})
        maturity = find(self.service, "Table 10", 6)["proposal"]["formula_corrections"]
        self.assertTrue(all(c["kind"] == "PROVEN_LOGIC_DEFECT" for c in maturity))
        by_coord = {c["coord"]: c["proposed"] for c in maturity}
        self.assertIn("reporting_date", by_coord["H6"])
        self.assertIn("Owner disposition", by_coord["D6"])

    def test_findings_queue_is_cell_level_and_classified(self):
        queue = self.service.catalog["findings_queue"]
        self.assertTrue(all(q["cell_found"] for q in queue))
        kinds = {q["finding_id"]: q["kind"] for q in queue}
        self.assertEqual(kinds["NBS-06"], "PROVEN_FORMULA_DEFECT")
        self.assertEqual(kinds["NBS-01"], "POLICY_MISMATCH")
        self.assertEqual(kinds["E02"], "MISSING_DEFINITION")
        self.assertEqual({q["cell"] for q in queue if q["finding_id"] == "E12"}, {"A559:A589", "B3", "B34"})
        self.assertFalse(next(q for q in queue if q["cell"] == "A1:V2135")["blocking"])


class DecisionTests(ServiceTestCase):
    def approve_everything_upstream(self):
        def approve_fields(doc):
            for field in doc["fields"].values():
                if field["system"] == "T24":
                    field.update(status="APPROVED", approved_by="Owner", approved_on="2026-10-14")
            doc["populations"]["LENDING_BASE"].update(status="APPROVED", approved_by="Owner", approved_on="2026-10-14")
        self.env.edit_config("report_selectors", approve_fields)

        def approve_policy(doc):
            doc["amount_bases"]["CLOSING_STOCK"]["approved"] = True
            doc["ecb_adapter"]["approved"] = True
        self.env.edit_config("calculation_policy", approve_policy)
        self.service.reload_config()

    def resolve_findings(self, business_id):
        for entry in self.service.catalog["findings_queue"]:
            if entry["business_id"] == business_id:
                self.service.decide_finding(entry["item_id"], "POLICY_DECIDED", **APPROVAL)

    def test_approvals_require_owner_date_reason_and_evidence(self):
        target = find(self.service, "Table 8", 20)["business_id"]
        for missing in ("actor", "reason", "approved_on", "approval_evidence"):
            with self.assertRaises(DecisionError, msg=missing):
                self.service.decide_mapping(target, "APPROVE_PROPOSAL", **{**APPROVAL, missing: ""})
        with self.assertRaises(DecisionError):
            self.service.decide_mapping(target, "APPROVE_PROPOSAL", **{**APPROVAL, "approved_on": "14/10/2026"})

    def test_no_proposal_becomes_effective_without_complete_inputs(self):
        target = find(self.service, "Table 8", 20)["business_id"]
        self.service.decide_mapping(target, "APPROVE_PROPOSAL", **APPROVAL)
        evaluation = self.service.evaluate(self.service.mapping(target))
        self.assertEqual(evaluation["state"], "APPROVED_BLOCKED")
        for reason in ("AMOUNT_BASIS_NOT_APPROVED:CLOSING_STOCK", "SELECTOR_FIELD_NOT_APPROVED:T24.CATEGORY",
                       "LENDING_POPULATION_NOT_APPROVED", "OPEN_FINDING:NBS-01"):
            self.assertIn(reason, evaluation["reasons"])
        self.approve_everything_upstream()
        self.resolve_findings(target)
        self.assertEqual(self.service.evaluate(self.service.mapping(target))["state"], "EFFECTIVE")
        self.assertEqual([e["business_id"] for e in self.service.effective_view()], [target])

    def test_free_text_proposal_without_selector_cannot_be_approved_as_proposal(self):
        ethix = find(self.service, "All Reports By Report ID_Templa", 13, "ETHIX")
        with self.assertRaises(DecisionError):
            self.service.decide_mapping(ethix["business_id"], "APPROVE_PROPOSAL", **APPROVAL)

    def test_owner_override_and_carrying_amount_stays_blocked_without_fees(self):
        self.approve_everything_upstream()
        ethix = find(self.service, "All Reports By Report ID_Templa", 33, "ETHIX")
        spec = {"metric_expression": "ETHIX_LOAN_CARRYING_AMOUNT", "amount_basis": "CLOSING_STOCK",
                "selectors": {"field": "T24.SECTOR", "op": "in", "values": ["4410"]},
                "nbs_target_business_ids": [ethix["nbs_row_candidates"][0]["business_id"]]}
        self.service.decide_mapping(ethix["business_id"], "APPROVE_OVERRIDE", spec=spec, **APPROVAL)
        reasons = self.service.evaluate(ethix)["reasons"]
        self.assertIn("METRIC_UNAVAILABLE:METRIC_UNDEFINED:LOAN_FEES", reasons)
        self.assertIn("SECTION_JOIN_NOT_APPROVED:BASE|Assets", reasons)
        with self.assertRaises(DecisionError):
            self.service.decide_mapping(ethix["business_id"], "APPROVE_OVERRIDE",
                                        spec={**spec, "nbs_target_business_ids": ["BM-notacandidate"]}, **APPROVAL)
        with self.assertRaises(DecisionError):
            self.service.decide_mapping(ethix["business_id"], "APPROVE_OVERRIDE",
                                        spec={**spec, "selectors": {"field": "ETHIX.SIC", "op": "in", "values": ["441"]}},
                                        **APPROVAL)

    def test_overrides_survive_refresh_and_changed_evidence_invalidates(self):
        t8 = find(self.service, "Table 8", 20)
        t9 = find(self.service, "Table 9", 10)
        self.service.decide_mapping(t8["business_id"], "APPROVE_PROPOSAL", **APPROVAL)
        self.service.decide_mapping(t9["business_id"], "DEFER", actor="Owner", reason="later")
        inventory_path = self.env.root / "supplied" / "source_inventory.json"
        inventory = json.loads(inventory_path.read_text(encoding="utf-8-sig"))
        # Insert a row above Table 8 row 20 (rows below shift) and change Table 8 B20's rule text.
        for row in inventory:
            if row["sheet"] == "Table 8" and row["source_row"] >= 5:
                row["source_row"] += 1
                for cell in row["raw_cells"].values():
                    cell["coord"] = cell["coord"].rstrip("0123456789") + str(row["source_row"])
            if row["sheet"] == "Table 8" and row["source_row"] == 21 and "B" in row["raw_cells"]:
                row["raw_cells"]["B"]["v"] += "\nPDODEFERREDPFT"
        inventory.reverse()  # sorting/order of evidence must not matter
        inventory_path.write_text(json.dumps(inventory), encoding="utf-8")
        result = self.service.refresh(use_supplied_inventory=True, note="changed evidence")
        self.assertIn(t8["business_id"], result["changes"]["changed"])
        self.assertEqual(result["changes"]["added"], [])
        self.assertEqual(result["changes"]["removed"], [])
        moved = self.service.mapping(t8["business_id"])
        self.assertEqual(moved["source_row"], 21)
        self.assertEqual(self.service.evaluate(moved)["state"], "STALE")
        self.assertEqual(self.service.evaluate(self.service.mapping(t9["business_id"]))["validity"], "CURRENT")
        stale = [d for d in self.service.decision_rows() if d["validity"] == "STALE"]
        self.assertEqual([d["subject_id"] for d in stale], [t8["business_id"]])

    def test_rollback_appends_history(self):
        target = find(self.service, "Table 8", 20)["business_id"]
        self.service.decide_mapping(target, "APPROVE_PROPOSAL", **APPROVAL)
        self.service.decide_mapping(target, "REJECT", **APPROVAL)
        restored = self.service.store.rollback("MAPPING", target, 1, "Owner", "undo reject")
        self.assertEqual((restored["version"], restored["action"], restored["rollback_of_version"]), (3, "APPROVE_PROPOSAL", 1))
        self.assertIsNone(self.service.store.rollback("MAPPING", target, 0, "Owner", "clear"))
        self.assertIsNone(self.service.store.current("MAPPING", target))
        self.assertEqual(len(self.service.store.history("MAPPING", target)), 4)

    def test_repeated_block_requires_owner_block_choice(self):
        self.approve_everything_upstream()
        table6 = next(s for s in self.service.catalog["sections"] if s["identity"] == "T6|R104")
        block2_row = next(m for m in self.service.catalog["mappings"]
                          if m["block_key"] == "T24|TABLE 6|B2" and m["kind"] == "RULE")
        spec = {"metric_expression": "OUTSTANDING", "amount_basis": "CLOSING_STOCK",
                "selectors": {"field": "T24.CATEGORY", "op": "in", "values": ["1500"]}}
        self.service.decide_mapping(block2_row["business_id"], "APPROVE_OVERRIDE", spec=spec, **APPROVAL)
        self.assertIn("SECTION_JOIN_NOT_APPROVED:T6|R104", self.service.evaluate(block2_row)["reasons"])
        with self.assertRaises(DecisionError):
            self.service.decide_section(table6["section_id"], "APPROVE_JOIN", block_keys=["T24|TABLE 7|B1"], **APPROVAL)
        self.service.decide_section(table6["section_id"], "APPROVE_JOIN", block_keys=["T24|TABLE 6|B1"], **APPROVAL)
        self.assertIn("BLOCK_NOT_IN_APPROVED_JOIN:T24|TABLE 6|B2", self.service.evaluate(block2_row)["reasons"])
        self.service.decide_section(table6["section_id"], "APPROVE_JOIN", block_keys=["T24|TABLE 6|B2"], **APPROVAL)
        reasons = self.service.evaluate(block2_row)["reasons"]
        self.assertFalse([r for r in reasons if "JOIN" in r])

    def test_clm_dependency_blocks_selectors_that_reach_3713(self):
        self.approve_everything_upstream()
        others = find(self.service, "Table 8", 27)
        self.service.decide_mapping(others["business_id"], "APPROVE_PROPOSAL", **APPROVAL)
        reasons = self.service.evaluate(others)["reasons"]
        self.assertIn("CLM_CREDIT_GROUP_NOT_APPROVED", reasons)
        self.assertIn("CLM_EMBEDDING_IN_VIRTUAL_BALANCES_UNVERIFIED", reasons)


class ExportTests(ServiceTestCase):
    def test_three_separate_exports_and_workbook(self):
        target = find(self.service, "Table 8", 20)["business_id"]
        self.service.decide_mapping(target, "APPROVE_PROPOSAL", **APPROVAL)
        written = export_all(self.service, self.env.root / "exports")
        approved = json.loads(Path(written["approved_mapping_config"]).read_text(encoding="utf-8"))
        self.assertEqual(approved["mapping_count"], 0)  # approved but blocked is not exported as executable
        self.assertIn("not bank reconciliation", approved["statement"])
        unresolved = Path(written["unresolved_exceptions"]).read_text(encoding="utf-8-sig")
        self.assertIn("LOAN_FEES", unresolved)
        self.assertIn("T38|R303", unresolved)
        diff = Path(written["source_vs_proposed"]).read_text(encoding="utf-8-sig")
        self.assertIn("PDOACCOUNT", diff)
        workbook = openpyxl.load_workbook(written["owner_review_workbook"])
        self.assertIn("Owner decisions", workbook.sheetnames)
        ws = workbook["Owner decisions"]
        formulas = [c for row in ws.iter_rows(min_row=2) for c in row if c.data_type == "f"]
        self.assertEqual(formulas, [])  # legacy formulas exported as inert text

    def test_owner_workbook_round_trip_is_validated(self):
        path = export_owner_workbook(self.service, self.env.root / "review.xlsx")
        t8 = find(self.service, "Table 8", 20)["business_id"]
        t9 = find(self.service, "Table 9", 10)["business_id"]
        workbook = openpyxl.load_workbook(path)
        ws = workbook["Owner decisions"]
        column = {name: index + 1 for index, name in enumerate(DECISION_COLUMNS)}
        rows = {ws.cell(r, 1).value: r for r in range(2, ws.max_row + 1)}
        r = rows[t8]
        for name, value in (("Action", "APPROVE_PROPOSAL"), ("Owner", "Report Owner"), ("Approved on", "2026-10-14"),
                            ("Reason", "matches owner dictionary"), ("Approval evidence", "minute 7")):
            ws.cell(r, column[name]).value = value
        r9 = rows[t9]
        ws.cell(r9, column["Action"]).value = "APPROVE_OVERRIDE"
        ws.cell(r9, column["Owner"]).value = "Report Owner"
        ws.cell(r9, column["Approved on"]).value = "2026-10-14"
        ws.cell(r9, column["Reason"]).value = "x"
        ws.cell(r9, column["Approval evidence"]).value = "minute 7"
        ws.cell(r9, column["Selectors (JSON)"]).value = "__import__('os')"
        ws.cell(r9, column["Evidence fingerprint"]).value = "0" * 64
        workbook.save(path)
        result = import_owner_workbook(self.service, path)
        self.assertEqual(result["applied"], [t8])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("STALE", result["errors"][0]["error"])
        self.assertEqual(self.service.store.current("MAPPING", t8)["origin"], "WORKBOOK_IMPORT")

    def test_starter_review_workbook_decisions_are_review_notes_only(self):
        source = ROOT.parent / "NBS_Mapping_Review.xlsx"
        if not source.exists():
            self.skipTest("starter review workbook not present")
        result = import_legacy_review_workbook(self.service, source)
        self.assertEqual(result["recorded_as_review_notes"], [])  # all PENDING in the supplied workbook


class ConfigTests(ServiceTestCase):
    def test_config_changes_are_validated_versioned_and_restorable(self):
        directory = self.env.root / "config"
        original = (directory / "calculation_policy.json").read_text(encoding="utf-8")
        doc = json.loads(original)
        doc["maturity"]["buckets"][1]["min_days"] = 9  # gap
        with self.assertRaises(ConfigError):
            save_config("calculation_policy", json.dumps(doc), "Owner", "bad", directory)
        doc = json.loads(original)
        doc["metrics"]["LOAN_FEES"] = {"kind": "COMPOSITE", "expression": "LOAN_FEES", "amount_basis": "CLOSING_STOCK"}
        with self.assertRaises(ConfigError):
            save_config("calculation_policy", json.dumps(doc), "Owner", "self reference", directory)
        rules = json.loads((directory / "balance_rules.json").read_text(encoding="utf-8"))
        rules["groups"]["OUTSTANDING"].append("DEFERREDPFT")  # duplicate membership
        with self.assertRaises(ConfigError):
            save_config("balance_rules", json.dumps(rules), "Owner", "dup", directory)
        rules = json.loads((directory / "balance_rules.json").read_text(encoding="utf-8"))
        rules["clm"]["extra_balances"][0].update(owner_approved=True, approved_by="Owner", approved_on="2026-10-14")
        save_config("balance_rules", json.dumps(rules), "Owner", "approve CREDIT group", directory)
        history = config_history(directory)
        self.assertEqual(history[-1]["reason"], "approve CREDIT group")
        stamp = sorted((directory / "history").glob("balance_rules.*.json"))[0].name.split(".")[1]
        restore_config("balance_rules", stamp, "Owner", "revert", directory)
        restored = json.loads((directory / "balance_rules.json").read_text(encoding="utf-8"))
        self.assertFalse(restored["clm"]["extra_balances"][0]["owner_approved"])


if __name__ == "__main__":
    unittest.main()
