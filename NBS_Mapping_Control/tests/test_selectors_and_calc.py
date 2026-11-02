"""Structured selectors (no eval), component expressions and report calculation policies."""

import unittest
from decimal import Decimal

from nbs_control.report_calc import (compute_report_rows, contract_metric, credit_quality_totals, maturity_state,
                                     metric_status, validate_maturity_buckets)
from nbs_control.selectors import (SelectorError, compile_selector, draft_category_selector, format_expression,
                                   parse_expression, validate_selector)
import mapping_engine

from tests.helpers import config_docs

FIELDS = {
    "T24.CATEGORY": {"system": "T24", "value_type": "integer_code", "status": "APPROVED"},
    "T24.SECTOR": {"system": "T24", "value_type": "integer_code", "status": "PROPOSED"},
    "ETHIX.SIC": {"system": "ETHIX", "value_type": "code", "status": "LEGACY_EVIDENCE"},
}


class SelectorTests(unittest.TestCase):
    def test_compiled_selector_partitions_and_reports_missing_attributes(self):
        selector = {"all": [{"field": "T24.CATEGORY", "op": "range", "min": 3000, "max": 3999},
                            {"field": "T24.CATEGORY", "op": "not_in", "values": ["3701", "3713"]}]}
        predicate = compile_selector(selector, FIELDS)
        self.assertTrue(predicate({"T24.CATEGORY": "3705"}))
        self.assertFalse(predicate({"T24.CATEGORY": "3713"}))
        self.assertFalse(predicate({"T24.CATEGORY": "6050"}))
        self.assertIsNone(predicate({}))

    def test_free_text_is_data_never_code(self):
        payload = "__import__('os').system('echo pwned')"
        predicate = compile_selector({"field": "T24.CATEGORY", "op": "eq", "value": payload}, FIELDS)
        self.assertFalse(predicate({"T24.CATEGORY": "3701"}))
        self.assertTrue(predicate({"T24.CATEGORY": payload}))
        with self.assertRaises(SelectorError):
            validate_selector({"field": "T24.CATEGORY", "op": "eval", "values": ["1"]}, FIELDS)
        with self.assertRaises(SelectorError):
            validate_selector({"sql": "SELECT * FROM ECB"}, FIELDS)

    def test_legacy_unknown_and_unapproved_fields_are_rejected(self):
        with self.assertRaises(SelectorError):
            validate_selector({"field": "ETHIX.SIC", "op": "in", "values": ["441"]}, FIELDS)
        with self.assertRaises(SelectorError):
            validate_selector({"field": "T24.NOPE", "op": "in", "values": ["1"]}, FIELDS)
        with self.assertRaises(SelectorError):
            validate_selector({"field": "T24.SECTOR", "op": "in", "values": ["1"]}, FIELDS, require_approved=True)
        self.assertEqual(validate_selector({"field": "T24.SECTOR", "op": "in", "values": ["1"]}, FIELDS,
                                           require_approved=False), {"T24.SECTOR"})

    def test_expression_parser_is_strict(self):
        self.assertEqual(parse_expression("OUTSTANDING + AMORTIZED_EARNED - 2*LOAN_FEES"),
                         [(Decimal(1), "OUTSTANDING"), (Decimal(1), "AMORTIZED_EARNED"), (Decimal(-2), "LOAN_FEES")])
        self.assertEqual(format_expression(parse_expression("A - B")), "A - B")
        for bad in ("", "OUTSTANDING AMORTIZED_EARNED", "OUTSTANDING + OUTSTANDING", "os.system('x')", "A + (B)"):
            with self.assertRaises(ValueError):
                parse_expression(bad)

    def test_legacy_category_drafts_are_narrow(self):
        self.assertEqual(draft_category_selector("CATEGORY=  3701, 3717, 3704 > ASSET TYPE = CURACCOUNT"),
                         {"field": "T24.CATEGORY", "op": "in", "values": ["3701", "3717", "3704"]})
        drafted = draft_category_selector("CATEGORY =3000 - 3999 BUT NOT EQUAL TO CATEGORY 3701, 3717 &  ASSET")
        self.assertEqual(drafted["all"][0], {"field": "T24.CATEGORY", "op": "range", "min": 3000, "max": 3999})
        self.assertIsNone(draft_category_selector("from all loan file NonPersonal all sic code start by 441"))


class MaturityTests(unittest.TestCase):
    def setUp(self):
        self.buckets = config_docs()["calculation_policy"]["maturity"]["buckets"]

    def test_configured_buckets_are_exclusive_and_complete(self):
        self.assertEqual(validate_maturity_buckets(self.buckets), [])
        for days in range(0, 9000):
            hits = [b["code"] for b in self.buckets
                    if days >= b["min_days"] and (b["max_days"] is None or days <= b["max_days"])]
            self.assertEqual(len(hits), 1, days)

    def test_reporting_date_basis_direction_and_separate_states(self):
        self.assertEqual(maturity_state("2027-01-14", "2026-10-06", self.buckets), "M3_TO_M6")  # +100 days
        self.assertEqual(maturity_state("2026-10-06", "2026-10-06", self.buckets), "UP_TO_1_WEEK")
        self.assertEqual(maturity_state("2026-10-13", "2026-10-06", self.buckets), "UP_TO_1_WEEK")
        self.assertEqual(maturity_state("2026-10-14", "2026-10-06", self.buckets), "W1_TO_M1")
        self.assertEqual(maturity_state("2026-10-05", "2026-10-06", self.buckets), "MATURED_OR_OVERDUE")
        self.assertEqual(maturity_state(None, "2026-10-06", self.buckets), "MISSING_MATURITY_DATE")
        self.assertEqual(maturity_state("2047-01-01", "2026-10-06", self.buckets), "OVER_Y20")

    def test_gaps_overlaps_and_closed_ends_are_rejected(self):
        gap = [{"code": "A", "min_days": 0, "max_days": 7}, {"code": "B", "min_days": 9, "max_days": None}]
        overlap = [{"code": "A", "min_days": 0, "max_days": 7}, {"code": "B", "min_days": 7, "max_days": None}]
        closed = [{"code": "A", "min_days": 0, "max_days": 7}]
        for buckets in (gap, overlap, closed):
            self.assertTrue(validate_maturity_buckets(buckets))


class CreditQualityTests(unittest.TestCase):
    def setUp(self):
        self.totals = config_docs()["calculation_policy"]["credit_quality"]["totals"]

    def test_totals_use_same_row_detail_columns_once(self):
        detail = {k: Decimal(v) for k, v in dict(B=100, D=20, H=30, J=40, L=50, C=10, E=2, I=3, K=4, M=5).items()}
        result = credit_quality_totals(detail, self.totals)
        self.assertEqual(result["F"], Decimal(120))
        self.assertEqual(result["N"], Decimal(120))   # legacy formula gave 260
        self.assertEqual(result["P"], Decimal(240))   # legacy formula gave 360
        self.assertEqual(result["G"], Decimal(12))
        self.assertEqual(result["O"], Decimal(12))    # legacy formula gave 392
        self.assertEqual(result["Q"], Decimal(24))    # legacy formula gave 382

    def test_missing_detail_makes_dependent_totals_unavailable(self):
        detail = {k: Decimal(1) for k in "BCDEHIJKLM"}
        detail["J"] = None
        result = credit_quality_totals(detail, self.totals)
        self.assertIsNone(result["N"]); self.assertIsNone(result["P"])
        self.assertEqual(result["F"], Decimal(2)); self.assertEqual(result["Q"], Decimal(5))


class MetricTests(unittest.TestCase):
    def setUp(self):
        docs = config_docs()
        self.policy = docs["calculation_policy"]
        self.rules = mapping_engine.validate_rules(docs["balance_rules"])
        self.contract = {"contract_id": "L1", "company": "CO", "source_system": "T24", "currency": "QAR",
                         "as_of": "2026-10-06", "group_totals_for_supplied_records":
                             {"OUTSTANDING": "-100.10", "AMORTIZED_EARNED": "-5.05", "UNEARNED_PROFIT": "7.00"}}

    def test_missing_fees_keep_carrying_amount_unavailable(self):
        status = metric_status("ETHIX_LOAN_CARRYING_AMOUNT", self.policy, self.rules)
        self.assertFalse(status["available"])
        self.assertIn("METRIC_UNDEFINED:LOAN_FEES", status["reasons"])
        value, reasons = contract_metric(self.contract, "ETHIX_LOAN_CARRYING_AMOUNT", self.policy)
        self.assertIsNone(value)  # never zero-filled
        self.assertEqual(reasons, ["METRIC_UNDEFINED:LOAN_FEES"])
        self.assertEqual(contract_metric(self.contract, "OUTSTANDING", self.policy), (Decimal("-100.10"), []))

    def test_fee_definition_would_compose_all_three_without_unearned(self):
        policy = dict(self.policy)
        policy["metrics"] = dict(self.policy["metrics"])
        policy["metrics"]["LOAN_FEES"] = {"kind": "COMPOSITE", "expression": "AMORTIZED_EARNED", "amount_basis": "CLOSING_STOCK"}
        value, reasons = contract_metric(self.contract, "ETHIX_LOAN_CARRYING_AMOUNT", policy)
        self.assertEqual(reasons, [])
        self.assertEqual(value, Decimal("-110.20"))  # UNEARNED_PROFIT is not added or deducted

    def _rows(self, specs, contracts, attributes):
        fields = {"T24.CATEGORY": {"system": "T24", "value_type": "integer_code", "status": "APPROVED"}}
        effective = [{"business_id": f"BM-{i}", "effective_spec": spec} for i, spec in enumerate(specs)]
        return compute_report_rows(effective, {"contracts": contracts}, attributes, self.policy,
                                   lambda s: compile_selector(s, fields))

    def test_metric_exclusivity_blocks_double_counted_contracts(self):
        spec_a = {"metric_expression": "OUTSTANDING", "amount_basis": "CLOSING_STOCK", "exclusive_group": "T8-TYPE",
                  "selectors": {"field": "T24.CATEGORY", "op": "in", "values": ["3713"]}}
        spec_b = dict(spec_a, selectors={"field": "T24.CATEGORY", "op": "range", "min": 3000, "max": 3999})
        result = self._rows([spec_a, spec_b], [self.contract], {"L1": {"T24.CATEGORY": "3713"}})
        self.assertEqual(len(result["exclusivity_violations"]), 1)
        self.assertTrue(all(row["amount"] is None for row in result["rows"]))
        exclusive_b = dict(spec_b, selectors={"all": [spec_b["selectors"],
                                                      {"field": "T24.CATEGORY", "op": "not_in", "values": ["3713"]}]})
        result = self._rows([spec_a, exclusive_b], [self.contract], {"L1": {"T24.CATEGORY": "3713"}})
        self.assertEqual(result["exclusivity_violations"], [])
        self.assertEqual(result["rows"][0]["amount"], "-100.10")
        self.assertEqual(result["rows"][1]["amount"], "0")

    def test_period_movement_rows_never_use_closing_stock(self):
        spec = {"metric_expression": "PL_PERIOD_MOVEMENT", "amount_basis": "PERIOD_MOVEMENT_YTD",
                "selectors": {"field": "T24.CATEGORY", "op": "in", "values": ["3713"]}}
        result = self._rows([spec], [self.contract], {"L1": {"T24.CATEGORY": "3713"}})
        self.assertIsNone(result["rows"][0]["amount"])
        self.assertTrue(any(r.startswith("AMOUNT_BASIS_MISMATCH") for r in result["rows"][0]["reasons"]))

    def test_currencies_stay_separate_and_incomplete_contracts_block_rows(self):
        usd = dict(self.contract, contract_id="L2", currency="USD")
        incomplete = dict(self.contract, contract_id="L3", group_totals_for_supplied_records=None)
        spec = {"metric_expression": "OUTSTANDING", "amount_basis": "CLOSING_STOCK",
                "selectors": {"field": "T24.CATEGORY", "op": "in", "values": ["3701"]}}
        attrs = {c: {"T24.CATEGORY": "3701"} for c in ("L1", "L2", "L3")}
        result = self._rows([spec], [self.contract, usd], attrs)
        self.assertEqual({(r["currency"], r["amount"]) for r in result["rows"]}, {("QAR", "-100.10"), ("USD", "-100.10")})
        result = self._rows([spec], [self.contract, incomplete], attrs)
        self.assertIsNone(result["rows"][0]["amount"])
        self.assertIn("CONTRACT_INCOMPLETE:L3", result["rows"][0]["reasons"])
        result = self._rows([spec], [self.contract], {})
        self.assertIsNone(result["rows"][0]["amount"])


if __name__ == "__main__":
    unittest.main()
