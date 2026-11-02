"""Re-import parity with the originals (when present) and the review interface."""

import re
import unittest

from nbs_control import DEFAULT_SOURCES, importer

from tests.helpers import ROOT, Environment


@unittest.skipUnless(all(p.exists() for p in DEFAULT_SOURCES.values()), "original workbooks not on this machine")
class OriginalWorkbookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.imported = importer.import_sources(DEFAULT_SOURCES)

    def test_reimport_matches_supplied_inventory_exactly(self):
        result = importer.compare_with_supplied(cls_imported := self.imported,
                                                importer.load_supplied_inventory(ROOT / "source_inventory.json"))
        self.assertEqual(result["hash_match"], {"T24": True, "ETHIX": True})
        self.assertEqual((result["fresh_rows"], result["supplied_rows"]), (4013, 4013))
        self.assertEqual((result["only_in_fresh"], result["only_in_supplied"], result["value_differences"]), ([], [], []))
        self.assertEqual(result["notes_fresh"], 58)
        self.assertEqual(sum(len(b["sheets"]) for b in cls_imported.values()), 51)

    def test_merged_headers_and_aliases_are_captured(self):
        t24 = self.imported["T24"]
        table11 = next(s for s in t24["sheets"] if s["name"] == "Table 11")
        self.assertIn("B3:C3", table11["merged_ranges"])
        aliases = [c for r in self.imported["ETHIX"]["rows"] for c in r["raw_cells"].values() if "alias" in c]
        k358 = next(c for c in aliases if c["coord"] == "K358")
        self.assertEqual(k358["alias"]["status"], "RESOLVED")
        self.assertIn("100", k358["alias"]["value"])


class WebTests(unittest.TestCase):
    def setUp(self):
        from nbs_control.web import create_app
        self.env = Environment()
        self.service = self.env.service()
        self.app = create_app(self.service, export_dir=self.env.root / "exports")
        self.client = self.app.test_client()

    def tearDown(self):
        self.env.cleanup()

    def token(self, path="/"):
        page = self.client.get(path).get_data(as_text=True)
        match = re.search(r'name="csrf" value="([0-9a-f]+)"', page)
        if match:
            return match.group(1)
        with self.client.session_transaction() as session:
            return session["csrf"]

    def test_views_render(self):
        target = next(m for m in self.service.catalog["mappings"] if m["sheet"] == "Table 8" and m["source_row"] == 20)
        for path in ("/", "/mappings?view=proposed", "/mappings?view=rules&q=PDOACCOUNT", "/mappings?view=effective",
                     "/mappings?view=unresolved", "/decisions", "/unresolved", "/findings", "/sections", "/config",
                     "/config/balance_rules", "/exports", "/run", "/reports", "/reports/product-policies", "/setup", f"/mapping/{target['business_id']}"):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, path)
        page = self.client.get(f"/mapping/{target['business_id']}").get_data(as_text=True)
        self.assertIn("PDOACCOUNT", page)
        self.assertIn("NO_OWNER_DECISION", page)

    def test_ecb_review_run_page_renders_results(self):
        import io
        sample = (ROOT / "samples" / "ecb_sample_clm.json").read_bytes()
        response = self.client.post("/run", data={"csrf": self.token("/run"), "payload": (io.BytesIO(sample), "sample.json")},
                                    content_type="multipart/form-data")
        page = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("SYN-MUSAWAMA", page)
        self.assertIn("-1050.00", page)
        self.assertIn("UNLINKED_CLS_ACCOUNT", page)
        self.assertIn("CLM_EMBEDDING_IN_VIRTUAL_BALANCES_UNVERIFIED", page)

    def test_report_mapping_form_saves_a_versioned_rule(self):
        import json
        path=self.service.config_dir/'generation_rules.json'
        if not path.exists():self.skipTest('generation configuration unavailable')
        doc=json.loads(path.read_text(encoding='utf-8'))
        key,spec=next((k,v) for k,v in doc['rules'].items() if v['source']=='ECB_LOAN')
        url='/reports/mapping/'+key
        self.assertEqual(self.client.get(url).status_code,200)
        form={'csrf':self.token(url),'source':spec['source'],'measure':spec['measure'],'layout':spec.get('layout') or 'geo',
              'components':','.join(spec['components']),'filter':json.dumps(spec['filter']),
              'negative_filter':'null','factor':'1','enabled':'on','notes':'Interface round-trip test',
              'actor':'Test reviewer','reason':'Verify saved mapping and history'}
        response=self.client.post(url,data=form,follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assertIn('Mapping saved with history',response.get_data(as_text=True))
        saved=json.loads(path.read_text(encoding='utf-8'))['rules'][key]
        self.assertEqual(saved['notes'],['Interface round-trip test'])
        self.assertTrue(list((self.service.config_dir/'generation_history').glob('*.json')))

    def test_post_requires_csrf_and_records_decision(self):
        target = next(m for m in self.service.catalog["mappings"] if m["sheet"] == "Table 8" and m["source_row"] == 20)
        url = f"/mapping/{target['business_id']}"
        form = {"action": "APPROVE_PROPOSAL", "actor": "Owner", "reason": "ok", "approved_on": "2026-10-14",
                "approval_evidence": "minute 1"}
        self.assertEqual(self.client.post(url, data=form).status_code, 400)
        response = self.client.post(url, data={**form, "csrf": self.token(url)}, follow_redirects=True)
        self.assertIn("Decision recorded", response.get_data(as_text=True))
        self.assertEqual(self.service.store.current("MAPPING", target["business_id"])["action"], "APPROVE_PROPOSAL")


if __name__ == "__main__":
    unittest.main()
