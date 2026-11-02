"""ECB adapter: multivalue alignment, snapshot vs movements, CLM links, populations, exceptions."""

import unittest
from decimal import Decimal

from nbs_control.ecb_adapter import run_review

from tests.helpers import BASE, adapter_config, ecb_record, link


def amounts(types, **values):
    return [values.get(t, "0") for t in types]


def contract(result, contract_id):
    return next(c for c in result["contracts"] if c["contract_id"] == contract_id)


def kinds(result):
    return [e["kind"] for e in result["adapter"]["exceptions"]]


class NonClmTests(unittest.TestCase):
    def setUp(self):
        self.cfg = adapter_config()

    def run_payload(self, records, links=(), cfg=None):
        return run_review({"reporting_date": "2026-10-06", "ecb_records": records, "links": list(links)}, *(cfg or self.cfg))

    def test_reconstructs_signed_closing_from_aligned_multivalues(self):
        opening = amounts(BASE, CURACCOUNT="-1000.10", ACCPRINCIPALPFT="-0.1", DEFERREDPFT="5")
        credit = amounts(BASE, CURACCOUNT="150.05", ACCPRINCIPALPFT="-0.2")
        debit = amounts(BASE, CURACCOUNT="-200")
        result = self.run_payload([ecb_record("R1", "L1", "3701", opening=opening, credit=credit, debit=debit)])
        c = contract(result, "L1")
        self.assertTrue(c["complete_for_supplied_records_and_required_types"])
        self.assertEqual(c["group_totals_for_supplied_records"],
                         {"OUTSTANDING": "-1050.05", "AMORTIZED_EARNED": "-0.3", "UNEARNED_PROFIT": "5"})
        self.assertFalse(result["production_ready"])

    def test_decimal_precision_beyond_28_digits(self):
        opening = amounts(BASE, CURACCOUNT="12345678901234567890123456789.123456789", PREACCOUNT="0.000000001")
        result = self.run_payload([ecb_record("R1", "L1", "3701", opening=opening)])
        self.assertEqual(contract(result, "L1")["group_totals_for_supplied_records"]["OUTSTANDING"],
                         "12345678901234567890123456789.123456790")

    def test_negative_and_zero_amounts_keep_their_sign(self):
        opening = amounts(BASE, CURACCOUNT="-5", DEFERREDPFT="0.00")
        result = self.run_payload([ecb_record("R1", "L1", "3701", opening=opening)])
        totals = contract(result, "L1")["group_totals_for_supplied_records"]
        self.assertEqual(totals["OUTSTANDING"], "-5"); self.assertEqual(totals["UNEARNED_PROFIT"], "0.00")

    def test_multivalue_length_mismatch_is_rejected_not_exploded(self):
        record = ecb_record("R1", "L1", "3701")
        record["DEBIT.MVMT"] = record["DEBIT.MVMT"][:-1]
        result = self.run_payload([record])
        self.assertIn("ECB_RECORD_REJECTED", kinds(result))
        self.assertEqual(result["adapter"]["exceptions"][0]["reason"], "MULTIVALUE_LENGTH_MISMATCH")
        self.assertFalse(result["complete_for_supplied_records_and_required_types"])

    def test_missing_amount_in_array_is_rejected(self):
        record = ecb_record("R1", "L1", "3701")
        record["OPEN.BALANCE"][0] = None
        result = self.run_payload([record])
        self.assertEqual(result["adapter"]["exceptions"][0]["reason"], "INVALID_MULTIVALUE_ENTRY")
        record["OPEN.BALANCE"][0] = 1.5  # binary float money is refused as well
        self.assertEqual(self.run_payload([record])["adapter"]["exceptions"][0]["reason"], "INVALID_MULTIVALUE_ENTRY")

    def test_missing_balance_type_is_not_zero_unless_convention_approved(self):
        types = BASE[:-1]
        result = self.run_payload([ecb_record("R1", "L1", "3701", types=types)])
        c = contract(result, "L1")
        self.assertEqual(c["missing_required_balance_types"], ["ACCDEFERREDPFT"])
        self.assertIsNone(c["group_totals_for_supplied_records"])
        convention = {"approved_by": "Owner", "approved_on": "2026-10-14", "applies_to": "BASE_TYPES"}
        result = self.run_payload([ecb_record("R1", "L1", "3701", types=types)],
                                  cfg=adapter_config(sparse_zero_convention=convention))
        self.assertTrue(contract(result, "L1")["complete_for_supplied_records_and_required_types"])
        filled = [r for r in result["records"] if r["source_record"].get("zero_filled_by_convention")]
        self.assertEqual(len(filled), 1)

    def test_snapshot_mode_never_adds_movements_to_closing(self):
        record = ecb_record("R1", "L1", "3701", credit=amounts(BASE, CURACCOUNT="999"))
        record["CLOSING.BAL"] = amounts(BASE, CURACCOUNT="-100")
        fields = adapter_config()[2]["ecb_adapter"]["fields"] | {"closing": "CLOSING.BAL"}
        cfg = adapter_config(mode="CLOSING_SNAPSHOT", fields=fields)
        result = self.run_payload([record], cfg=cfg)
        self.assertEqual(contract(result, "L1")["group_totals_for_supplied_records"]["OUTSTANDING"], "-100")
        cfg_reconstruct = adapter_config(fields=fields)
        result = self.run_payload([record], cfg=cfg_reconstruct)
        self.assertEqual(result["adapter"]["exceptions"][0]["reason"], "CLOSING_AND_MOVEMENTS_BOTH_SUPPLIED_DOUBLE_COUNT_RISK")

    def test_repeated_snapshot_per_journal_entry_is_not_counted_twice(self):
        first = ecb_record("R1", "L1", "3701", opening=amounts(BASE, CURACCOUNT="10"), entry_ref="JE-1")
        second = ecb_record("R2", "L1", "3701", opening=amounts(BASE, CURACCOUNT="10"), entry_ref="JE-2")
        result = self.run_payload([first, second])
        reasons = [e["reason"] for e in result["adapter"]["exceptions"]]
        self.assertEqual(reasons, ["DUPLICATE_SNAPSHOT_FOR_CONTRACT_GRAIN"] * 2)
        self.assertEqual(result["contracts"], [])
        self.assertFalse(result["complete_for_supplied_records_and_required_types"])

    def test_currencies_and_dates_are_never_combined(self):
        qar = ecb_record("R1", "L1", "3701", opening=amounts(BASE, CURACCOUNT="10"))
        usd = ecb_record("R2", "L1", "3701", opening=amounts(BASE, CURACCOUNT="7"), currency="USD")
        result = self.run_payload([qar, usd])
        partitions = {p["currency"]: p["group_totals_for_supplied_records"]["OUTSTANDING"]
                      for p in result["partition_totals_for_supplied_records"]}
        self.assertEqual(partitions, {"QAR": "10", "USD": "7"})
        stale = ecb_record("R3", "L2", "3701", snapshot_as_of="2026-09-30")
        result = self.run_payload([stale])
        self.assertEqual(result["adapter"]["exceptions"][0]["reason"], "SNAPSHOT_DATE_NOT_REPORTING_DATE")
        value_dated = ecb_record("R4", "L3", "3701", date_basis="VALUE")
        self.assertEqual(self.run_payload([value_dated])["adapter"]["exceptions"][0]["reason"], "DATE_BASIS_MISMATCH")

    def test_unknown_sp_and_pdo_codes_are_unclassified_and_block(self):
        for code in ("PDOACCOUNT", "CURACCOUNTSP", "DUEPRINCIPALPFT", "NABPRINCIPALPFT", "PDODEFERREDPFT"):
            result = self.run_payload([ecb_record("R1", "L1", "3701", types=BASE + [code])])
            self.assertIn("UNCLASSIFIED_BALANCE_TYPE", kinds(result), code)
            self.assertIsNone(contract(result, "L1")["group_totals_for_supplied_records"], code)
        excluded = adapter_config(owner_excluded_balance_types=["PDOACCOUNT"])
        result = self.run_payload([ecb_record("R1", "L1", "3701", types=BASE + ["PDOACCOUNT"])], cfg=excluded)
        self.assertIn("OWNER_EXCLUDED_BALANCE_TYPE", kinds(result))
        self.assertTrue(contract(result, "L1")["complete_for_supplied_records_and_required_types"])

    def test_virtual_aggregate_plus_component_overlap_blocks(self):
        cfg = adapter_config(virtual={"TOTALOUTSTANDING": ["CURACCOUNT", "DUEACCOUNT"]})
        result = self.run_payload([ecb_record("R1", "L1", "3701", types=BASE + ["TOTALOUTSTANDING"])], cfg=cfg)
        self.assertIn("VIRTUAL_AGGREGATE_AND_COMPONENT_BOTH_PRESENT", kinds(result))
        self.assertIsNone(contract(result, "L1")["group_totals_for_supplied_records"])

    def test_non_lending_population_is_retained_as_exception(self):
        result = self.run_payload([ecb_record("R1", "DEP1", "6001", types=["CURACCOUNT"])])
        self.assertEqual(kinds(result), ["OUT_OF_SELECTED_POPULATION"])
        self.assertEqual(result["contracts"], [])


class ClmTests(unittest.TestCase):
    def payload(self, *, parent_category="3713", links=None, extra_records=(), parent_flag=None, child_types=None):
        parent = ecb_record("P1", "MUR-1", parent_category, opening=amounts(BASE, CURACCOUNT="-1000", ACCPRINCIPALPFT="-20"))
        if parent_flag is not None:
            parent["is_clm"] = parent_flag
        child = ecb_record("C1", "CLS-1", "6050", types=child_types or ["CREDIT", "ACCDEPOSITPFT"],
                           opening=["-300.50", "-4.25"][:len(child_types or [1, 2])])
        return {"reporting_date": "2026-10-06", "ecb_records": [parent, child, *extra_records],
                "links": [link()] if links is None else links}

    def test_verified_link_attaches_both_components_with_audit_trail(self):
        cfg = adapter_config(credit_approved=True, virtual={"UNRELATEDVIRTUAL": ["OTHERTYPE"]})
        result = run_review(self.payload(), *cfg)
        c = contract(result, "MUR-1")
        self.assertTrue(c["is_clm"])
        self.assertEqual(c["group_totals_for_supplied_records"],
                         {"OUTSTANDING": "-1300.50", "AMORTIZED_EARNED": "-24.25", "UNEARNED_PROFIT": "0"})
        self.assertEqual(c["linked_component_contract_ids"], ["CLS-1"])
        linked = [r for r in result["records"] if r["balance_type"] in ("CREDIT", "ACCDEPOSITPFT")]
        for row in linked:
            self.assertEqual(row["parent_contract_id"], "MUR-1")
            self.assertEqual(row["contract_id"], "CLS-1")
            self.assertEqual(row["source_record"]["relationship"]["evidence"], "test relationship")
            self.assertEqual(row["category"], "6050")
        self.assertTrue(result["complete_for_supplied_records_and_required_types"])

    def test_credit_pending_and_unverified_embedding_suppress_totals(self):
        result = run_review(self.payload(), *adapter_config())
        c = contract(result, "MUR-1")
        self.assertIsNone(c["group_totals_for_supplied_records"])
        self.assertIn("CLM_EMBEDDING_IN_VIRTUAL_BALANCES_UNVERIFIED", c["flags"])
        self.assertIn("RECORD_VALIDATION_FAILED", c["flags"])

    def test_component_embedded_in_selected_virtual_balance_is_rejected(self):
        cfg = adapter_config(credit_approved=True, virtual={"TOTALCLM": ["CREDIT"]})
        payload = self.payload()
        parent = payload["ecb_records"][0]
        parent["CURR.ASSET.TYPE"] = BASE + ["TOTALCLM"]
        for key in ("OPEN.BALANCE", "CREDIT.MVMT", "DEBIT.MVMT"):
            parent[key] = parent[key] + ["0"]
        result = run_review(payload, *cfg)
        self.assertIn("CLM_COMPONENT_ALREADY_EMBEDDED_IN_VIRTUAL_BALANCE", kinds(result))
        self.assertIsNone(contract(result, "MUR-1")["group_totals_for_supplied_records"])

    def test_category_3713_without_indicator_or_link_is_unresolved(self):
        result = run_review(self.payload(links=[]), *adapter_config(credit_approved=True, virtual={"X": ["Y"]}))
        c = contract(result, "MUR-1")
        self.assertIsNone(c["is_clm"])
        self.assertIn("CLM_STATUS_UNKNOWN", [f for r in result["records"] for f in r["flags"]])
        self.assertIn("UNLINKED_CLS_ACCOUNT", kinds(result))

    def test_category_3713_explicit_non_clm_is_ordinary_loan(self):
        payload = self.payload(links=[], parent_flag=False)
        result = run_review(payload, *adapter_config())
        c = contract(result, "MUR-1")
        self.assertFalse(c["is_clm"])
        self.assertEqual(c["group_totals_for_supplied_records"]["OUTSTANDING"], "-1000")
        self.assertIn("UNLINKED_CLS_ACCOUNT", kinds(result))  # 6050 never swept into a non-CLM loan

    def test_configured_indicator_conflicting_with_link_is_unresolved(self):
        cfg = adapter_config(credit_approved=True, virtual={"X": ["Y"]})
        cfg[1]["clm"].update(detector_field="L.CLM.FLAG", true_values=["Y"], false_values=["N"])
        payload = self.payload()
        payload["ecb_records"][0]["L.CLM.FLAG"] = "N"
        result = run_review(payload, *cfg)
        self.assertIn("CLM_STATUS_CONFLICT", kinds(result))
        self.assertIsNone(contract(result, "MUR-1")["is_clm"])
        payload["ecb_records"][0]["L.CLM.FLAG"] = "Y"
        self.assertTrue(contract(run_review(payload, *cfg), "MUR-1")["is_clm"])

    def test_category_3713_alone_or_other_parent_category_never_makes_clm(self):
        result = run_review(self.payload(parent_category="3701"), *adapter_config(credit_approved=True))
        self.assertIn("PARENT_SNAPSHOT_NOT_CATEGORY_3713", result["adapter"]["rejected_links"][0]["reasons"])
        self.assertFalse(contract(result, "MUR-1")["is_clm"])

    def test_child_linked_to_conflicting_parents_is_rejected(self):
        second_parent = ecb_record("P2", "MUR-2", "3713")
        links = [link(), link(parent="MUR-2", link_id="L2")]
        result = run_review(self.payload(links=links, extra_records=[second_parent]), *adapter_config(credit_approved=True))
        reasons = [r for l in result["adapter"]["rejected_links"] for r in l["reasons"]]
        self.assertEqual(reasons.count("CHILD_LINKED_TO_CONFLICTING_PARENTS"), 2)
        self.assertFalse(result["complete_for_supplied_records_and_required_types"])

    def test_duplicate_or_unverified_or_mismatched_links_are_rejected(self):
        cases = {
            "LINK_ID_MISSING_OR_REUSED": [link(), link()],
            "LINK_NOT_VERIFIED": [link(verified=False)],
            "LINK_CURRENCY_CONTEXT_MISMATCH": [link(currency="USD")],
            "LINK_DATE_MISMATCH": [link(as_of="2026-10-05")],
            "LINK_CHILD_PRODUCT_NOT_CLS": [link(child_product="DEPOSIT")],
            "LINK_EVIDENCE_MISSING": [link(evidence="")],
        }
        for reason, links in cases.items():
            result = run_review(self.payload(links=links), *adapter_config(credit_approved=True))
            found = [r for l in result["adapter"]["rejected_links"] for r in l["reasons"]]
            self.assertIn(reason, found, reason)
            self.assertFalse(result["complete_for_supplied_records_and_required_types"], reason)

    def test_parent_with_two_cls_children_needs_allocation_policy(self):
        child2 = ecb_record("C2", "CLS-2", "6050", types=["CREDIT", "ACCDEPOSITPFT"])
        links = [link(), link(child="CLS-2", link_id="L2")]
        result = run_review(self.payload(links=links, extra_records=[child2]), *adapter_config(credit_approved=True))
        found = [r for l in result["adapter"]["rejected_links"] for r in l["reasons"]]
        self.assertIn("PARENT_HAS_MULTIPLE_CLS_CHILDREN_NO_ALLOCATION_POLICY", found)

    def test_other_cls_balances_are_not_swept(self):
        payload = self.payload(child_types=["CREDIT", "ACCDEPOSITPFT", "CURACCOUNT"])
        payload["ecb_records"][1]["OPEN.BALANCE"] = ["-1", "-2", "-999"]
        result = run_review(payload, *adapter_config(credit_approved=True, virtual={"X": ["Y"]}))
        self.assertIn("CLS_BALANCE_NOT_IN_CLM_SCOPE", kinds(result))
        self.assertEqual(contract(result, "MUR-1")["group_totals_for_supplied_records"]["OUTSTANDING"], "-1001")


if __name__ == "__main__":
    unittest.main()
