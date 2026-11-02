# NBS rebuild handoff

Start with CLAUDE_NBS_REBUILD_BRIEF_20261017.md in the project root. It tells Claude to implement and verify the full exercise, using the exact new files and the inspection findings. The human review is exports/rebuild_review_20261017/NBS_SOURCE_REVIEW.md.

Updated owner clarification on 17 October 2026: the category extract dated 1 October represents 30 September balances. Use it in September reconstruction with effective reporting date 2026-09-30, preserving its raw dates. This supersedes the initial handoff's unresolved-date warning. The source-specific authority is in reporting_basis_owner_confirmation.json beside this README. Duplicate treatment, accounting purpose and completeness still require the checks in the brief.

This pack contains the three new original files in inputs, the coding brief and the review evidence. It is an addition to the existing NBS_Mapping_Control project, not a standalone completed application. The earlier ECB, loans, deposits, trial balance, mapping workbooks and old reference remain in their existing locations. Paths and hashes are recorded in the brief and manifests. File selection should be supported if Claude works on a different machine.

The current application and mapping configuration have not been changed by this inspection. No source SQL was executed. A confirmed maturity-column defect in the existing prototype requires correction. New BO values must remain comparison references rather than being copied into generated results.

To start Claude Code, use this instruction:

Read CLAUDE_NBS_REBUILD_BRIEF_20261017.md and exports/rebuild_review_20261017/NBS_SOURCE_REVIEW.md. I confirm that the category entries dated 1 October represent 30 September 2026 balances. Use that effective reporting date while preserving the raw dates. Implement the complete NBS rebuild and verification exercise described in the brief using this existing project. Keep mappings editable, resolve the repeated-entry and calculation issues, retain source and mapping history, and continue all supported work without waiting for routine approvals.

The optional review utilities are audit_rebuild_sources.py, analyze_bo_review.py and verify_rebuild_review.py. They run from the existing project root and need the earlier normalized bank database. They inspect source data and generate audit evidence; they do not repair the production application or run bank SQL.
