# Fixes and improvements implemented

Everything existing was kept: no module, page, command or configuration was removed. The pre-change baseline is commit `3dcb6ef` and can be recovered with `git checkout 3dcb6ef`.

## A. Corrections to existing code

| # | File | Before | After |
|---|---|---|---|
| A1 | `nbs_control/gl_mapping.py` `_token_filter` | Inline `1000-1999, 6001, 7001` became the literal value `1000-1999` and never matched | Parsed as an inclusive range OR list: `{'any': [{'op': 'in', 'values': ['6001', '7001']}, {'op': 'range', 'values': [1000, 1999]}]}`. Reversed or malformed ranges are reported, not ignored. Whitespace-separated lists still work. |
| A2 | `nbs_control/gl_mapping.py` `_balance_types` | `CURACCOUNT, DUEACCOUNT` became a single non-existent balance type | Split into atomic identifiers. Non-identifiers are reported. |
| A3 | `nbs_control/bank_data.py` | CONSOL_KEY positions hard-coded | Positions read from `config/tb_recon.json` (`consol_key_layouts.AC`), with the same defaults, so behaviour is unchanged. The run manifest records them (`consol_key_positions`). |
| A4 | `tests/test_rebuild.py` | 2 tests errored when the `.gitignore`-excluded legacy SQL CSV was absent | They skip with an explicit reason, like the other tests that need bank inputs. |

## B. New: whole-TB migration reconciliation (`nbs_control/tbrecon`, `tbrecon-1.0.0`)

Integrated into the existing CLI (`python -m nbs_control tb-recon …`) and web application (`/tb`, linked in the top menu).

### Engine A: PRODUCT_S3 / asset type (`engine_a.py`)
- Unpivots every non-zero `<TYPE>_BAL_QAR` column into an atomic component. Never a blanket sum. A blank cell counts as missing, not zero.
- Decodes CONSOL_KEY with the configurable AC layout. Parsed keys and rule matches are cached per (key, balance type).
- Rules must name atomic balance types; named groups (`*PRINCIPAL`) and lists are expanded. A rule without an atomic balance type is unusable and reported.
- Each rule balance type must exist in the source schema or be a validated alias (`balance_type_aliases`, target checked against the schema). Otherwise it is reported as `UNSUPPORTED_BALANCE_TYPE`, and the target GL is marked INCOMPLETE rather than treated as zero.
- Contra / BL types (`contra_balance_types`, `contra_balance_type_prefixes`) allocate only through a rule that names them explicitly. Otherwise they stay `CONTRA_UNRESOLVED`, separate from gross.
- Allocation grain `CONSOL_KEY + ATOMIC_BALANCE_TYPE + TARGET_GL` (`contributions.csv`). One key can feed several GLs through different balance types.
- `POSSIBLE_MAPPING_COLUMN_MISALIGNMENT` diagnostic: for each rule, flags a column (e.g. SECTOR) whose values never occur at that key segment but all occur at another (e.g. PRODUCT). It reports affected rules, rows, accounts, net / absolute amount, segment positions, verification state, examples and the current status of each affected component. When the source carries explicit dimension columns, it also compares them with the key segments. The UI column is not renamed: the evidence is reported and a correction is proposed.

### Engine B: INTERNAL_CUS_ACC (`engine_b.py`)
- Exact one-to-one mapping from source account to target account / GL. CONSOL_KEY is never read, required or generated (`consol_key_used: false`).
- Statuses: `MISSING_MAPPING`, `DUPLICATE_MAPPING` (conflicting rows), `INVALID_TARGET` (none or several GLs), `CUSTOMER_REF_UNRESOLVED`. Flags: `TARGET_ACCOUNT_CURRENCY_MISMATCH`, `TARGET_ACCOUNT_GL_DIFFERS_FROM_ACTUAL`.
- A populated `CUSTOMER_ACCOUNT_REF` is resolved through the authoritative customer-account mapping. This covers Nostro / Vostro without an extra flag.
- Optional account-level expected-versus-actual comparison (`target_accounts`). Many-to-one targets are reported.

### Engine C: PL (`engine_c.py`)
- Own PL key layout (validated tokens from `categ_data.py`). Explicit PL columns supply dimensions the layout lacks. Key-versus-column conflicts are counted.
- PL rules over PL category, product, department, sector, residence, currency and company. A rule needing a dimension the source cannot supply is reported as `DIMENSION_NOT_AVAILABLE`.
- No PL source gives `SOURCE_PENDING`. PL legacy TB lines are then **not** routed through the GL mapping (no false success).

### Rule compiler (`criteria.py`, `rules.py`)
- Exact values, comma / semicolon / newline OR lists, inclusive integer ranges, prefixes, named ranges (`*NAME`).
- Blank means UNRESTRICTED (configurable to MUST_BE_BLANK). `*` / `ANY` means explicit unrestricted. `<BLANK>` means the value must be empty.
- GL Report H / D / T lines, continuation rows (blank RULE_ID), `^` inheritance and configurable inherited blank columns.
- Precedence is (PRIORITY, restricted dimensions, exact-only dimensions). Equally specific matches with different targets return `AMBIGUOUS`, never the first rule.
- Multi-target rules return `MULTI_TARGET_UNRESOLVED`: never the first GL, an equal split or a forced zero.
- Static diagnostics: duplicate rules, conflicting duplicates, duplicate line IDs, invalid rules, criteria on non-detail lines.

### Whole-TB aggregation (`tb.py`)
- The legacy TB line is covered by an account-level population (linked by `LEGACY_GL`). The gap between TB and population is a `MISSING_SOURCE_RECORD` exception and is never allocated.
- Uncovered lines form the labelled DIRECT stream, mapped only when the GL mapping has exactly one target. With several targets they stay `MULTI_TARGET_ALLOCATION_UNRESOLVED`.
- An engine target outside the authorised legacy GL mapping gives a `WRONG_TARGET_GL` (rule-level) exception.
- Per target GL and currency: legacy GL(s), expected (by stream A / B / C / D), actual closing, validated post-COB movements, actual opening, net and absolute difference, unresolved candidate amount, mapping status, reconciliation status (`RECONCILED`, `DIFFERENCE`, `EXPECTED_ONLY`, `ACTUAL_ONLY`, `INCOMPLETE`, `SOURCE_PENDING`) and reason.
- Roll-forward: opening migrated (expected) + validated post-COB movements = computed closing, compared with actual closing. Movements on or before cutover, after the TB date or not validated are excluded with a reason.
- GL Report reconstruction: detail lines from components first, then totals (`TOTAL_OF` lists and `A..B` ranges, nested totals, circularity detected).
- Benchmark (`TrialBalance_withConsolKey.csv`) is compared independently and never used as a source.

### Root cause, worklist, controls
- `rootcause.py` classifies every unallocated amount (component, rule and legacy-GL levels) and every open GL residual into the 17 categories of the brief, kept by level so money is not counted twice. GL residuals are tested in order: excluded movements (timing), exact sign reversal, offsetting pairs (wrong target GL / currency), population gap, then open items whose candidates include the GL (exact subset-sum, otherwise partial with LOW confidence), then unmapped legacy amount, then actual-TB discrepancy or genuine unexplained.
- Systemic issues: grouped root causes with records, accounts, net and absolute amount, related rules, proposed action, confidence and open question.
- Proposed correction worklist with original value, proposed value, reason, evidence, amount and confidence. Approved mapping files are never changed. Only mechanical, evidence-backed column corrections are `auto_applicable`, and they apply to a **copy** (`--apply-proposals`), stored as a new rule version.
- `controls.py`: C01 completeness and duplicates; C02 totals before / after normalisation (exact Decimal); C03 balance-type totals; C04 coverage; C05 expected versus actual; C05B source → mapping → expected walk (no amount disappears); C06 multi-target cardinality; C07 currency; C08 sign and contra; C09 business-date integrity; C10 reproducibility (result hash compared with the previous run on identical inputs, or an in-process re-run); C11 benchmark; C12 CONSOL_KEY layout verification.

### Persistence, exports, UI
- `data/tbrecon/runs.sqlite` records each run (input SHA-256s, config hash, rules hash, result hash, reproducibility, statistics) and each content-addressed rule version.
- Per run in `exports/tb_recon/<run>/`: indexed `run.sqlite` for drill-down, `reconciliation.xlsx` (15 sheets), `report.html`, `audit.json`, and CSVs (TB, exceptions, root causes, worklist, components, allocation grain, GL Report, roll-forward, controls, legacy lines, unallocated, benchmark, misalignment, rule diagnostics, internal accounts).
- Web: run form (background thread, so the UI does not freeze), synthetic dataset creation, run list, TB view filtered by BS / PL / OBS, currency, status and GL, GL drill-down (allocation grain, components, unresolved candidates, roll-forward, exceptions), account / arrangement / balance-type view, root causes and exceptions, worklist, rules / misalignment / layout / GL Report / benchmark, and before-and-after comparison.
- CLI: `tb-recon`, `tb-recon --legacy-semantics` (BEFORE measurement), `tb-recon --apply-proposals`, `tb-recon-synthetic`, `tb-recon-compare`, `tb-recon-runs`. Exit codes: 0 fully reconciled, 2 open items or missing inputs, 1 input error.

## C. Supporting changes
- `config/tb_recon.json`: layouts with per-segment `verified` and `evidence`, aliases, contra types, criteria semantics, sign convention, tolerance, cutover date.
- `Start_TB_Reconciliation.cmd`: Windows launcher (offline wheels; opens `/tb`).
- `build_release.py`: builds the versioned release ZIP without confidential data or runtime databases.
- `.gitignore`: `data/tbrecon/` and `exports/tb_recon/` stay local.
- `tests/test_tbrecon.py`: 45 regression tests.
