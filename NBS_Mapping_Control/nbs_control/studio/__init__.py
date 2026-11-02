"""NBS Mapping Studio: Excel-driven mapping validation, BO report reconciliation and evidence-backed corrections.

The mapping workbook is the authority: its own conditions are compiled (with exact cell references) and
executed. The BO-generated report is reconciled against the allocation those conditions produce. Proposed
corrections are verified by re-executing the workbook with the edit applied; the original workbook is never
changed - approved corrections are written to a separate, verified copy.
"""

STUDIO_VERSION = 'studio-1.0.0'
