"""NBS mapping control: import, owner review and deterministic component mapping.

Nothing in this package connects to a bank, evaluates workbook text or formulas,
or certifies an NBS report. Owner decisions are application state, not proof of
bank reconciliation.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
EXPORT_DIR = PROJECT_ROOT / "exports"

# Original mapping workbooks for the owner-review catalog: looked up in <app>/inputs (portable), never a fixed user folder.
DEFAULT_SOURCES = {
    "T24": PROJECT_ROOT / "inputs" / "NBS MAPPING - 6 Oct 2026.xlsx",
    "ETHIX": PROJECT_ROOT / "inputs" / "NBS01 Mapping (Ehab).xlsx",
}
