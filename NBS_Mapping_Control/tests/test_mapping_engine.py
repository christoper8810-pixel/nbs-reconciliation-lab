"""Acceptance tests for explicit rules and review-only aggregation safeguards."""
import copy
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from mapping_engine import RuleError, aggregate, classify, load_records, load_rules, parse_money, validate_rules


BASE_RULES = {
    "groups": {
        "OUTSTANDING": ["CURACCOUNT", "PREACCOUNT", "GRCACCOUNT", "DELACCOUNT", "NABACCOUNT", "DUEACCOUNT",
                        "DELDEFERREDPFT", "GRCDEFERREDPFT", "NABDEFERREDPFT", "DUEDEFERREDPFT",
                        "RECDEFERREDPFT", "PREDEFERREDPFT"],
        "AMORTIZED_EARNED": ["ACCPRINCIPALPFT", "RECPRINCIPALPFT", "GRCPRINCIPALPFT", "DELPRINCIPALPFT",
                             "PREPRINCIPALPFT"],
        "UNEARNED_PROFIT": ["DEFERREDPFT", "ACCDEFERREDPFT"],
    },
    "clm": {"detector_field": None, "true_values": [], "extra_balances": []},
}


def clm_rules():
    """Synthetic test tokens only. They are not proposed Temenos type names."""
    raw = copy.deepcopy(BASE_RULES)
    raw["clm"]["extra_balances"] = [
        {"balance_type": "TEST_CLM_ONE", "group": "OUTSTANDING", "basis": "OWNER_APPROVED",
         "owner_approved": True, "approved_by": "Test owner", "approved_on": "2026-10-14"},
        {"balance_type": "TEST_CLM_TWO", "group": "UNEARNED_PROFIT", "basis": "OWNER_APPROVED",
         "owner_approved": True, "approved_by": "Test owner", "approved_on": "2026-10-14"},
    ]
    raw["valid_balance_types"] = [code for values in raw["groups"].values() for code in values]
    raw["valid_balance_types"] += ["TEST_CLM_ONE", "TEST_CLM_TWO"]
    return raw


def records_for(rules, *, company="NBS01", currency="QAR", source="T24", contract="LOAN1", clm=False,
                category=None, amount="0"):
    types = list(rules["membership"])
    if clm:
        types += list(rules["extra_membership"])
    records = [
        {"company": company, "currency": currency, "as_of": "2026-10-06", "source_system": source,
         "contract_id": contract, "balance_type": code, "is_clm": clm,
         "category": category, "record_id": f"{source}-{currency}-{contract}-{i}",
         "signed_closing_balance": amount}
        for i, code in enumerate(types)
    ]
    if clm:
        for row in records:
            if row["balance_type"] in rules["extra_membership"]:
                row.update(contract_id=f"{contract}-CLS", parent_contract_id=contract,
                           parent_category="3713", category="6050", component_origin="CLS", verified_link=True)
    return records


class MappingTests(unittest.TestCase):
    def setUp(self):
        self.rules = validate_rules(BASE_RULES)

    def test_all_19_base_memberships_are_exact(self):
        self.assertEqual(len(self.rules["membership"]), 19)
        for group, codes in BASE_RULES["groups"].items():
            for code in codes:
                result = classify(self.rules, f"  {code.lower()}  ", False)
                self.assertEqual(result["group"], group)
                self.assertTrue(result["ready_for_mapping"])
                self.assertFalse(result["production_ready"])

    def test_unknown_prefix_suffix_sp_and_pdo_have_no_alias(self):
        for code in ("CURACCOUNTPDO", "CURACCOUNTSP", "SPCURACCOUNT", "CUR ACCOUNT", "PDO", "SP"):
            result = classify(self.rules, code, False)
            self.assertIsNone(result["group"])
            self.assertIn("UNKNOWN_BALANCE_TYPE", result["flags"])

    def test_unknown_clm_retains_base_group_but_blocks_readiness(self):
        result = classify(self.rules, "CURACCOUNT", "unknown", "3713")
        self.assertEqual(result["group"], "OUTSTANDING")
        self.assertFalse(result["ready_for_mapping"])
        self.assertIn("CLM_STATUS_UNKNOWN", result["flags"])

    def test_category_3713_does_not_infer_clm(self):
        result = classify(self.rules, "CURACCOUNT", False, "3713")
        self.assertTrue(result["ready_for_mapping"])
        self.assertFalse(result["is_clm"])

    def test_clm_true_without_configured_extras_fails_closed(self):
        result = classify(self.rules, "CURACCOUNT", True, "3713")
        self.assertEqual(result["group"], "OUTSTANDING")
        self.assertIn("CLM_TWO_EXTRA_TYPES_NOT_CONFIGURED", result["flags"])
        self.assertFalse(result["ready_for_mapping"])

    def test_two_configured_extras_apply_only_to_confirmed_clm_scope(self):
        rules = validate_rules(clm_rules())
        self.assertEqual(classify(rules, "TEST_CLM_ONE", True, "6050", parent_category="3713",
                                 component_origin="CLS", verified_link=True)["group"], "OUTSTANDING")
        self.assertTrue(classify(rules, "TEST_CLM_TWO", True, "6050", parent_category="3713",
                                component_origin="CLS", verified_link=True)["ready_for_mapping"])
        for clm in (False, None):
            self.assertIsNone(classify(rules, "TEST_CLM_ONE", clm, "3713")["group"])
        self.assertIn("CLM_SCOPE_MISMATCH", classify(rules, "CURACCOUNT", True, "3714")["flags"])
        self.assertIn("CLM_SCOPE_UNVERIFIED", classify(rules, "CURACCOUNT", True)["flags"])

    def test_ethix_same_spelling_still_requires_crosswalk(self):
        result = classify(self.rules, "CURACCOUNT", False, source_system="ETHIX")
        self.assertIsNone(result["group"])
        self.assertIn("ETHIX_CROSSWALK_NOT_APPROVED", result["flags"])
        raw = copy.deepcopy(BASE_RULES)
        raw["ethix_crosswalk"] = {"approved_by": "Test owner", "approved_on": "2026-10-14",
                                  "mappings": {"LEGACY_FINANCE": "CURACCOUNT"}}
        rules = validate_rules(raw)
        result = classify(rules, "legacy_finance", False, source_system="ETHIX")
        self.assertEqual(result["balance_type"], "CURACCOUNT")
        self.assertEqual(result["group"], "OUTSTANDING")
        self.assertIsNone(classify(rules, "CURACCOUNT", False, source_system="ETHIX")["group"])

    def test_invalid_rule_configurations(self):
        invalids = []
        raw = copy.deepcopy(BASE_RULES)
        raw["groups"]["UNEARNED_PROFIT"].append("curaccount")
        invalids.append(raw)
        for extras in (
            [{"balance_type": "X", "group": "OUTSTANDING"}],
            [{"balance_type": "X", "group": "OUTSTANDING"}, {"balance_type": "X", "group": "UNEARNED_PROFIT"}],
            [{"balance_type": "CURACCOUNT", "group": "OUTSTANDING"}, {"balance_type": "X", "group": "UNEARNED_PROFIT"}],
            [{"balance_type": "X", "group": "WRONG"}, {"balance_type": "Y", "group": "UNEARNED_PROFIT"}],
        ):
            raw = copy.deepcopy(BASE_RULES)
            raw["clm"]["extra_balances"] = extras
            invalids.append(raw)
        raw = clm_rules()
        raw["valid_balance_types"].remove("TEST_CLM_ONE")
        invalids.append(raw)
        raw = copy.deepcopy(BASE_RULES)
        raw["ethix_crosswalk"] = {"mappings": {"X": "CURACCOUNT"}}
        invalids.append(raw)
        for raw in invalids:
            with self.assertRaises(RuleError):
                validate_rules(raw)

    def test_exact_decimal_and_signed_closing_balance_aggregation(self):
        records = records_for(self.rules)
        records[0]["signed_closing_balance"] = "-100.10"
        records[1]["signed_closing_balance"] = "0.20"
        records[2]["signed_closing_balance"] = "0.10"
        report = aggregate(self.rules, records)
        self.assertTrue(report["complete_for_supplied_records_and_required_types"])
        self.assertEqual(report["contracts"][0]["group_totals_for_supplied_records"]["OUTSTANDING"], "-99.80")
        self.assertFalse(report["production_ready"])
        records[0]["signed_closing_balance"] = "999999999999999999999999999999999.10"
        totals = aggregate(self.rules, records)["contracts"][0]["group_totals_for_supplied_records"]
        self.assertEqual(totals["OUTSTANDING"], "999999999999999999999999999999999.40")

    def test_missing_balance_is_never_zero_filled(self):
        records = records_for(self.rules)
        report = aggregate(self.rules, records[:-1])
        self.assertFalse(report["complete_for_supplied_records_and_required_types"])
        self.assertIsNone(report["partition_totals_for_supplied_records"])
        self.assertIsNone(report["contracts"][0]["group_totals_for_supplied_records"])
        self.assertEqual(report["contracts"][0]["missing_required_balance_types"], ["ACCDEFERREDPFT"])

    def test_duplicate_record_and_grain_block_both_rows(self):
        records = records_for(self.rules)
        duplicate = dict(records[0])
        report = aggregate(self.rules, records + [duplicate])
        self.assertEqual(report["rejected_record_count"], 2)
        self.assertIsNone(report["contracts"][0]["group_totals_for_supplied_records"])
        for row in (report["records"][0], report["records"][-1]):
            self.assertIn("DUPLICATE_RECORD_ID", row["flags"])
            self.assertIn("DUPLICATE_CONTRACT_BALANCE_GRAIN", row["flags"])

    def test_duplicate_grain_even_with_different_record_ids(self):
        records = records_for(self.rules)
        duplicate = dict(records[0], record_id="OTHER_ID")
        report = aggregate(self.rules, records + [duplicate])
        self.assertIn("DUPLICATE_CONTRACT_BALANCE_GRAIN", report["records"][-1]["flags"])

    def test_missing_and_ambiguous_records_block_totals(self):
        records = records_for(self.rules)
        del records[0]["record_id"]
        records[1]["signed_closing_balance"] = "1,000.00"
        records[2]["is_clm"] = "N"
        report = aggregate(self.rules, records)
        self.assertFalse(report["complete_for_supplied_records_and_required_types"])
        self.assertIsNone(report["contracts"][0]["group_totals_for_supplied_records"])

    def test_mixed_contract_clm_flags_block_totals(self):
        records = records_for(self.rules)
        records[0]["is_clm"] = True
        records[0]["category"] = "3713"
        report = aggregate(self.rules, records)
        self.assertIn("MIXED_CONTRACT_CLM_FLAGS", report["contracts"][0]["flags"])
        self.assertIsNone(report["contracts"][0]["group_totals_for_supplied_records"])

    def test_clm_requires_all_21_types(self):
        rules = validate_rules(clm_rules())
        records = records_for(rules, clm=True, category="3713")
        self.assertTrue(aggregate(rules, records)["complete_for_supplied_records_and_required_types"])
        report = aggregate(rules, records[:-1])
        self.assertIn("TEST_CLM_TWO", report["contracts"][0]["missing_required_balance_types"])
        self.assertIsNone(report["contracts"][0]["group_totals_for_supplied_records"])

    def test_clm_linked_components_bucket_under_parent_and_retain_component_ids(self):
        rules = validate_rules(clm_rules())
        records = records_for(rules, clm=True, category="3713")
        records[-2]["signed_closing_balance"] = "-2.25"
        records[-1]["signed_closing_balance"] = "0.15"
        report = aggregate(rules, records)
        self.assertEqual(len(report["contracts"]), 1)
        parent = report["contracts"][0]
        self.assertEqual(parent["contract_id"], "LOAN1")
        self.assertEqual(parent["linked_component_contract_ids"], ["LOAN1-CLS"])
        self.assertEqual(parent["group_totals_for_supplied_records"]["OUTSTANDING"], "-2.25")
        self.assertEqual(report["records"][-1]["contract_id"], "LOAN1-CLS")
        self.assertEqual(report["records"][-1]["report_contract_id"], "LOAN1")

    def test_clm_link_scope_requires_all_explicit_evidence(self):
        rules = validate_rules(clm_rules())
        for field, invalid in (("category", "6051"), ("parent_category", "3714"),
                               ("component_origin", "OTHER"), ("verified_link", False),
                               ("parent_contract_id", "")):
            records = records_for(rules, clm=True, category="3713")
            records[-1][field] = invalid
            report = aggregate(rules, records)
            self.assertFalse(report["complete_for_supplied_records_and_required_types"], field)
            self.assertIsNone(report["partition_totals_for_supplied_records"], field)

    def test_clm_extra_without_present_confirmed_parent_blocks_total(self):
        rules = validate_rules(clm_rules())
        records = records_for(rules, clm=True, category="3713")[-2:]
        report = aggregate(rules, records)
        self.assertIn("CLM_EXTRA_PARENT_NOT_PRESENT_OR_CONFIRMED", report["contracts"][0]["flags"])
        self.assertIsNone(report["contracts"][0]["group_totals_for_supplied_records"])

    def test_clm_component_reused_by_two_parents_blocks_both(self):
        rules = validate_rules(clm_rules())
        first = records_for(rules, clm=True, category="3713", contract="LOAN1")
        second = records_for(rules, clm=True, category="3713", contract="LOAN2")
        for row in second[-2:]:
            row["contract_id"] = "LOAN1-CLS"
        report = aggregate(rules, first + second)
        self.assertFalse(report["complete_for_supplied_records_and_required_types"])
        self.assertTrue(all(contract["group_totals_for_supplied_records"] is None for contract in report["contracts"]))
        self.assertIn("CLM_LINKED_COMPONENT_REUSED_ACROSS_PARENTS", report["records"][-1]["flags"])

    def test_clm_component_can_change_parent_across_as_of_dates(self):
        rules = validate_rules(clm_rules())
        first = records_for(rules, clm=True, category="3713", contract="LOAN1")
        second = records_for(rules, clm=True, category="3713", contract="LOAN2")
        for row in second:
            row["as_of"] = "2026-10-07"
        for row in second[-2:]:
            row["contract_id"] = "LOAN1-CLS"
        report = aggregate(rules, first + second)
        self.assertTrue(report["complete_for_supplied_records_and_required_types"])
        self.assertEqual(len(report["contracts"]), 2)
        self.assertTrue(all(contract["group_totals_for_supplied_records"] is not None for contract in report["contracts"]))

    def test_clm_component_same_date_conflicting_parents_cross_currency_blocks(self):
        rules = validate_rules(clm_rules())
        first = records_for(rules, clm=True, category="3713", contract="LOAN1", currency="QAR")
        second = records_for(rules, clm=True, category="3713", contract="LOAN2", currency="USD")
        for row in second[-2:]:
            row["contract_id"] = "LOAN1-CLS"
        report = aggregate(rules, first + second)
        self.assertFalse(report["complete_for_supplied_records_and_required_types"])
        self.assertIsNone(report["partition_totals_for_supplied_records"])
        self.assertIn("CLM_LINKED_COMPONENT_REUSED_ACROSS_PARENTS", report["records"][-1]["flags"])

    def test_clm_extra_pair_cannot_be_split_between_two_components(self):
        rules = validate_rules(clm_rules())
        records = records_for(rules, clm=True, category="3713")
        records[-2]["contract_id"] = "CLS_A"
        records[-1]["contract_id"] = "CLS_B"
        report = aggregate(rules, records)
        self.assertEqual(report["contracts"][0]["missing_required_balance_types"], [])
        self.assertFalse(report["complete_for_supplied_records_and_required_types"])
        self.assertIn("CLM_EXTRA_BALANCES_FROM_DIFFERENT_COMPONENT_CONTRACTS", report["contracts"][0]["flags"])
        self.assertIsNone(report["contracts"][0]["group_totals_for_supplied_records"])
        self.assertIsNone(report["partition_totals_for_supplied_records"])

    def test_unapproved_inferred_grouping_blocks_totals(self):
        raw = clm_rules()
        raw["clm"]["extra_balances"][0].update(basis="INFERRED_REVIEW_REQUIRED", owner_approved=False,
                                               approved_by=None, approved_on=None)
        rules = validate_rules(raw)
        report = aggregate(rules, records_for(rules, clm=True, category="3713"))
        self.assertFalse(report["complete_for_supplied_records_and_required_types"])
        self.assertIn("CLM_GROUP_ASSIGNMENT_REQUIRES_OWNER_APPROVAL", report["records"][-2]["flags"])
        self.assertIsNone(report["contracts"][0]["group_totals_for_supplied_records"])

    def test_unknown_type_blocks_totals_despite_all_required_types_present(self):
        records = records_for(self.rules)
        records.append(dict(records[0], balance_type="CURACCOUNTPDO", record_id="BAD"))
        report = aggregate(self.rules, records)
        self.assertFalse(report["complete_for_supplied_records_and_required_types"])
        self.assertIsNone(report["partition_totals_for_supplied_records"])
        self.assertIsNone(report["contracts"][0]["group_totals_for_supplied_records"])

    def test_currency_company_date_and_source_partition_separation(self):
        records = records_for(self.rules, currency="QAR", amount="1")
        records += records_for(self.rules, currency="USD", amount="2")
        records += records_for(self.rules, source="TRANSACT", currency="QAR", amount="3")
        records += records_for(self.rules, company="NBS02", currency="QAR", contract="LOAN2", amount="4")
        report = aggregate(self.rules, records)
        self.assertTrue(report["complete_for_supplied_records_and_required_types"])
        partitions = report["partition_totals_for_supplied_records"]
        self.assertEqual(len(partitions), 4)
        lookup = {(p["company"], p["currency"], p["source_system"]): p for p in partitions}
        self.assertEqual(lookup[("NBS01", "QAR", "T24")]["group_totals_for_supplied_records"]["OUTSTANDING"], "12")
        self.assertEqual(lookup[("NBS01", "USD", "T24")]["group_totals_for_supplied_records"]["OUTSTANDING"], "24")
        self.assertEqual(lookup[("NBS01", "QAR", "TRANSACT")]["group_totals_for_supplied_records"]["OUTSTANDING"], "36")

    def test_ethix_can_never_implicitly_classify_or_claim_equivalence(self):
        records = records_for(self.rules, source="ETHIX")
        report = aggregate(self.rules, records)
        self.assertIsNone(report["partition_totals_for_supplied_records"])
        self.assertFalse(report["ethix_valuation_equivalence_verified"])

    def test_decimal_parser_rejects_formula_float_and_nan(self):
        for value in (1.1, True, "=1+2", "NaN", "1,23", "1e4", None):
            with self.assertRaises(ValueError):
                parse_money(value)
        self.assertEqual(parse_money(" -1.20 "), Decimal("-1.20"))

    def test_file_loaders_preserve_json_decimal_and_reject_ambiguous_csv(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            path = Path(directory) / "records.json"
            path.write_text('[{"signed_closing_balance":0.1}]', encoding="utf-8")
            self.assertEqual(load_records(path)[0]["signed_closing_balance"], Decimal("0.1"))
            path.write_text('[{"record_id":"1","record_id":"2"}]', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_records(path)
            csv_path = Path(directory) / "records.csv"
            csv_path.write_text("balance_type,balance_type\nCURACCOUNT,PREACCOUNT\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_records(csv_path)
            csv_path.write_text("balance_type,signed_closing_balance\nCURACCOUNT,1,000\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_records(csv_path)

    def test_empty_input_has_no_complete_totals(self):
        report = aggregate(self.rules, [])
        self.assertFalse(report["complete_for_supplied_records_and_required_types"])
        self.assertIsNone(report["partition_totals_for_supplied_records"])


class DeliveredRuleTests(unittest.TestCase):
    """Integration acceptance tests for the actual owner draft shipped in this pack."""

    def setUp(self):
        self.path = Path(__file__).resolve().parent.parent / "config" / "balance_rules.json"
        self.rules = load_rules(self.path)

    def test_delivered_group_counts_and_clm_scopes(self):
        self.assertEqual({group: len(codes) for group, codes in self.rules["groups"].items()},
                         {"OUTSTANDING": 12, "AMORTIZED_EARNED": 5, "UNEARNED_PROFIT": 2})
        self.assertEqual(self.rules["candidate_category"], "3713")
        self.assertEqual(self.rules["source_category"], "6050")
        self.assertEqual(self.rules["source_product"], "CLS")
        self.assertEqual(set(self.rules["extra_membership"]), {"CREDIT", "ACCDEPOSITPFT"})

    def test_actual_credit_is_scoped_candidate_with_approval_pending(self):
        result = classify(self.rules, "CREDIT", True, "6050", parent_category="3713",
                          component_origin="CLS", verified_link=True)
        self.assertEqual(result["candidate_group"], "OUTSTANDING")
        self.assertEqual(result["group"], "OUTSTANDING")
        self.assertFalse(result["ready_for_mapping"])
        self.assertEqual(result["grouping_basis"], "INFERRED_REVIEW_REQUIRED")
        self.assertIn("CLM_GROUP_ASSIGNMENT_REQUIRES_OWNER_APPROVAL", result["flags"])
        self.assertFalse(result["grouping_approval"]["owner_approved"])

    def test_actual_accrued_deposit_profit_is_accepted_only_in_scope(self):
        result = classify(self.rules, "ACCDEPOSITPFT", True, "6050", parent_category="3713",
                          component_origin="CLS", verified_link=True)
        self.assertEqual(result["group"], "AMORTIZED_EARNED")
        self.assertEqual(result["grouping_basis"], "USER_ACCRUED_PROFIT")
        self.assertTrue(result["ready_for_mapping"])
        self.assertTrue(result["grouping_approval"]["owner_approved"])
        self.assertFalse(result["production_ready"])

    def test_actual_extras_reject_generic_deposits_nonclm_and_unlinked_components(self):
        for code in ("CREDIT", "ACCDEPOSITPFT"):
            for parameters in (
                {"is_clm": True, "category": "6100", "parent_category": "3713",
                 "component_origin": "CLS", "verified_link": True},
                {"is_clm": False, "category": "6050", "parent_category": "3713",
                 "component_origin": "CLS", "verified_link": True},
                {"is_clm": True, "category": "6050", "parent_category": "3713",
                 "component_origin": "CLS", "verified_link": False},
                {"is_clm": True, "category": "6050"},
            ):
                result = classify(self.rules, code, **parameters)
                self.assertIsNone(result["group"], (code, parameters))
                self.assertFalse(result["ready_for_mapping"], (code, parameters))

    def test_full_actual_21_linked_records_have_no_totals_with_credit_pending(self):
        records = records_for(self.rules, clm=True, category="3713")
        self.assertEqual(len(records), 21)
        report = aggregate(self.rules, records)
        self.assertEqual(len(report["contracts"]), 1)
        self.assertEqual(report["contracts"][0]["contract_id"], "LOAN1")
        self.assertEqual(report["contracts"][0]["missing_required_balance_types"], [])
        self.assertFalse(report["complete_for_supplied_records_and_required_types"])
        self.assertIsNone(report["partition_totals_for_supplied_records"])
        self.assertIsNone(report["contracts"][0]["group_totals_for_supplied_records"])
        credit_row = next(row for row in report["records"] if row["balance_type"] == "CREDIT")
        self.assertIn("CLM_GROUP_ASSIGNMENT_REQUIRES_OWNER_APPROVAL", credit_row["flags"])

    def test_disposable_actual_credit_approval_yields_exact_parent_totals(self):
        original_bytes = self.path.read_bytes()
        raw = json.loads(original_bytes.decode("utf-8-sig"))
        credit_rule = next(rule for rule in raw["clm"]["extra_balances"] if rule["balance_type"] == "CREDIT")
        credit_rule.update(owner_approved=True, approved_by="Disposable test owner", approved_on="2026-10-14")
        rules = validate_rules(raw)
        records = records_for(rules, clm=True, category="3713")
        amounts = {"CURACCOUNT": "100.10", "ACCPRINCIPALPFT": "2.25", "DEFERREDPFT": "-30.00",
                   "CREDIT": "-10.20", "ACCDEPOSITPFT": "0.15"}
        for row in records:
            row["signed_closing_balance"] = amounts.get(row["balance_type"], "0")
        report = aggregate(rules, records)
        self.assertTrue(report["complete_for_supplied_records_and_required_types"])
        self.assertEqual(report["contracts"][0]["group_totals_for_supplied_records"],
                         {"OUTSTANDING": "89.90", "AMORTIZED_EARNED": "2.40", "UNEARNED_PROFIT": "-30.00"})
        self.assertEqual(report["contracts"][0]["linked_component_contract_ids"], ["LOAN1-CLS"])
        self.assertFalse(report["production_ready"])
        self.assertFalse(report["population_and_source_extraction_verified"])
        self.assertEqual(self.path.read_bytes(), original_bytes)


if __name__ == "__main__":
    unittest.main()
