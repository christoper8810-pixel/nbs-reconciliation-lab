# Mapping Studio: baseline, implementation and validation

## 1. Baseline (what existed before this update)

Established from the source code (Git commits `3dcb6ef` and `289c59b`):

- **Version:** the application had no release number. The Mapping Studio component is now versioned `studio-1.0.0`.
- **Workbook condition handling:** the GL mapping workbook was read by `nbs_control/gl_mapping.py` at **fixed column letters**:
  - GL Report columns A–R, with named ranges in O–R;
  - CATEGORY, SEGMENT and GL Mapping at fixed letters.

  It stored the criteria as text and used them only to draft parts of NBS report lines (`line_parts`). It did not:
  - execute the conditions against source records, or reconstruct a GL-report allocation;
  - reconcile a BO report against the conditions;
  - validate across sheets, or support exclusions, wildcards, comparisons, continuation-row inheritance or cross-sheet formula references;
  - propose corrections.

  Inline ranges and listed balance types were mis-read; this was fixed in the TB release.
- **The existing "BO" feature** (`bo_reference.py`, `rebuild_compare.py`) compares a generated NBS report with the Ethix BO NBS workbook by QCB item code. It is kept unchanged.
- **The TB reconciliation** added by the previous instruction (`nbs_control/tbrecon`) is a separate tool. It stays available as "TB reconciliation (separate tool)" in the menu and does not define this project. Mapping Studio reuses only its generic table reader and CONSOL_KEY layout.

## 2. Synthetic validation: the real workbook and BO report were not available

`nbs_control/studio/synthetic.py` builds a mapping workbook in the layout the existing adapter reads:
- GL Report with a named-range table; CATEGORY, SEGMENT, COA, BRANCH and GL Mapping (letters A/B/C/E/H/L/W);
- a cross-sheet formula, a workbook defined name, comments, number formats and merged cells;
- 141 source records and a BO report.

The generator computes the true BO allocation itself, independently of the Studio engine.

### Clean scenario
The expected allocation equals the independent truth on every key (Decimal equality). All 19 BO keys match, and no correction is proposed.

### Defect scenario: 8 workbook defects and 4 BO-side defects injected

| ID | Injected defect | Studio result |
|---|---|---|
| W1 | `GL Report!G4` category `3700-3748` (true `3700-3749`) | Proposal G4 → `3700-3749`, **HIGH**. 14 records, closes DKBGL1020 QAR exactly. Alternative cell G5 listed. |
| W2 | `GL Report!G7` lacks 3901 | Proposal G7 → `3700-3749, 3901`, **HIGH** |
| W3 | `GL Mapping!W2` sends fixed assets to DKBGL1070 | Proposal W2 → `DKBGL1060`, **HIGH** (both lines close) |
| W4 | `GL Report!G18` reversed range `6099-6001` | Rule reported not executable; proposal → `6001-6099`, **HIGH**, confirmed by BO |
| W7 | `GL Report!J6` sector `1999-2999` overlaps the retail line | Overlap reported; proposal → `2000-2999`, **HIGH** |
| W8 | category 3955 not in CATEGORY | `UNKNOWN_CATEGORY` finding (no value invented) → Finance worklist |
| W9 | `GL Mapping!W3` `DKBGL 1065` | `GLMAP_UNKNOWN_LINE`; proposal → `DKBGL1065`, **HIGH** |
| W12 | product 4101 written in SECTOR `J13` | `POSSIBLE_MAPPING_COLUMN_MISALIGNMENT`; proposal J13 → blank, S13 (PRODUCT) → `4101`, **HIGH** |
| W5 | BO duplicate row on DKBGL2010 | `DUPLICATE_BO_ROWS`, responsibility BO_REPORT (not a mapping change); BO total ≠ sum of details flagged |
| W6 | BO sign reversed on DKBGL5010 | `SIGN_PRESENTATION`, BO_REPORT |
| W10 | BO line DKBGL9999 not in the workbook | `LINE_NOT_IN_MAPPING`, MAPPING_OR_BO |
| W11 | BO amount on DKBGL2040, no source record | `NO_SOURCE_RECORDS_FOR_LINE`, SOURCE_DATA, UNRESOLVED with the evidence request |

No false proposals were made. Every proposal is verified by re-executing the workbook. Edits that would leave records outside every line, or create a double allocation, are never proposed.

| Statistic | Before | After approving the 7 HIGH proposals and rerunning on the corrected copy |
|---|---|---|
| BO keys matched | 5 of 23 | 16 of 21 (the remaining 5 are the BO-side, source-side and W8 items above) |
| Absolute difference (detail lines) | 10,195,583.71 | 3,790,467.95 (BO duplicate, BO sign, BO-only lines) |
| Proposals | 7 HIGH | none (nothing left that a mapping change explains) |
| Corrected copy | – | 8 cells changed. 269 other cells compared with the original: values, formulas, number formats, comments and merged cells unchanged. Original file SHA-256 unchanged. |

### Performance
| Source records | Distinct signatures | Analysis time (cloud container) |
|---|---|---|
| 141 | 72 | < 1 s |
| 40,000 | 8,835 | 5.1 s |
| 200,000 | 9,043 | 9.1 s |

## 3. What remains unverified

- **Real workbook layout:** column recognition is by header text, with the existing adapter's letter positions as a disclosed fall-back. The first real run must be checked on the *Compiled workbook conditions* page. Any "used by position – verify" or "header not recognised" line needs confirmation.
- **Real BO report layout and amount presentation:** line and amount column names, unit (thousands?), sign and whether totals are included. The Studio detects global scale and sign patterns and reports them, but never applies them automatically.
- **Precedence between overlapping lines:** whether the bank's BO process counts a record matched by two lines in both (`ALL`, the default, flagged) or in one (`MOST_SPECIFIC`) is a setting; the real behaviour is not known.
- **Formulas:** formulas other than direct cell or name references, saved without calculated values, are reported as not executable.
