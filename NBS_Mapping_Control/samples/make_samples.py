"""Generate the synthetic ECB sample used by the run guide and tests. Not bank data."""

import json
from pathlib import Path

BASE = ["CURACCOUNT", "PREACCOUNT", "GRCACCOUNT", "DELACCOUNT", "NABACCOUNT", "DUEACCOUNT", "DELDEFERREDPFT",
        "GRCDEFERREDPFT", "NABDEFERREDPFT", "DUEDEFERREDPFT", "RECDEFERREDPFT", "PREDEFERREDPFT", "ACCPRINCIPALPFT",
        "RECPRINCIPALPFT", "GRCPRINCIPALPFT", "DELPRINCIPALPFT", "PREPRINCIPALPFT", "DEFERREDPFT", "ACCDEFERREDPFT"]


def ecb(record_id, contract, category, types, opening, credit, debit, **extra):
    return {"record_id": record_id, "company": "SYNTHETIC_CO", "source_system": "T24", "contract_id": contract,
            "currency": "QAR", "snapshot_as_of": "2026-10-06", "date_basis": "BOOK", "category": category,
            "CURR.ASSET.TYPE": types, "OPEN.BALANCE": opening, "CREDIT.MVMT": credit, "DEBIT.MVMT": debit, **extra}


def build():
    zeros = ["0.00"] * len(BASE)
    opening = list(zeros); opening[0] = "-1000.00"; opening[12] = "-25.50"; opening[17] = "300.00"
    debit = list(zeros); debit[0] = "-200.00"
    credit = list(zeros); credit[0] = "150.00"
    return {
        "example_kind": "SYNTHETIC ONLY - not bank data",
        "reporting_date": "2026-10-06",
        "ecb_records": [
            ecb("ECB-MUR-1", "SYN-MURABAHA-CLM", "3713", BASE, opening, credit, debit),
            ecb("ECB-CLS-1", "SYN-CLS-1", "6050", ["CREDIT", "ACCDEPOSITPFT", "OTHERCLSBAL"],
                ["-500.00", "-12.34", "9.99"], ["0.00", "0.00", "0.00"], ["0.00", "0.00", "0.00"]),
            ecb("ECB-MUS-1", "SYN-MUSAWAMA", "3701", BASE, opening, credit, debit),
            ecb("ECB-CLS-UNLINKED", "SYN-CLS-ORPHAN", "6050", ["CREDIT"], ["-77.00"], ["0.00"], ["0.00"]),
            ecb("ECB-DEP-1", "SYN-DEPOSIT", "6001", ["CURACCOUNT"], ["900.00"], ["0.00"], ["0.00"]),
        ],
        "links": [
            {"link_id": "LINK-1", "company": "SYNTHETIC_CO", "source_system": "T24", "as_of": "2026-10-06",
             "currency": "QAR", "parent_contract_id": "SYN-MURABAHA-CLM", "parent_category": "3713",
             "child_contract_id": "SYN-CLS-1", "child_category": "6050", "child_product": "CLS", "verified": True,
             "evidence": "SYNTHETIC: placeholder for the bank's arrangement-to-CLS relationship record"},
        ],
    }


if __name__ == "__main__":
    target = Path(__file__).with_name("ecb_sample_clm.json")
    target.write_text(json.dumps(build(), indent=2) + "\n", encoding="utf-8")
    print(target)
