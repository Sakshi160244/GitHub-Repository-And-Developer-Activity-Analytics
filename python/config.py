from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
CLEANED_DATA_DIR = BASE_DIR / "data" / "cleaned"
CHART_DIR = BASE_DIR / "visualizations"

# Analysis reference time, not the collection date.
AS_OF_DATE = pd.Timestamp("2026-09-15", tz="UTC")

USERNAME = "Sakshi160244"
SEARCH_QUERY = "topic:data-analysis stars:>5"

ACTIVITY_ORDER = [
    "Active",
    "Moderately Active",
    "Inactive",
    "Unknown"
]

ACTIVITY_COLORS = {
    "Active": "#59A14F",
    "Moderately Active": "#F28E2B",
    "Inactive": "#E15759",
    "Unknown": "#79706E"
}