"""
03_sheets_connector.py
======================
Step 3 — External API Connector (Google Sheets)

Reads fetch_parameters.json produced by Step 2, connects to Google Sheets
to pull KPI data from the correct month tab, and writes kpi_data.json
for Step 4 (AI Completion) to consume.

Modes:
    python 03_sheets_connector.py           # real Sheets API (needs credentials)
    python 03_sheets_connector.py --mock    # mock data (for testing, no credentials needed)

Google Sheets Setup (one-time):
    1. Go to https://console.cloud.google.com
    2. Enable "Google Sheets API" and "Google Drive API"
    3. Create a Service Account → download JSON key
    4. Save the key as:  credentials/service_account.json
    5. Share your Google Sheet with the service account email
    6. Set SPREADSHEET_ID below (from the sheet URL)
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration  — update these before using real mode
# ---------------------------------------------------------------------------

BASE_DIR          = Path(__file__).parent
FETCH_PARAMS_FILE = BASE_DIR / "fetch_parameters.json"     # input  (from Step 2)
KPI_DATA_FILE     = BASE_DIR / "kpi_data.json"             # output (for Step 4)
CREDENTIALS_FILE  = BASE_DIR / "credentials" / "service_account.json"

# ← Replace with your actual Google Sheet ID (from its URL)
SPREADSHEET_ID = "1yUA_qXREhg41Z3OEiwMMGrAPHnnd4-B2RCSLWRAfdEM"

# Columns to read from the sheet (A1 notation range)
DATA_RANGE = "A1:B10"

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Mock data — simulates what a real sheet would return
# ---------------------------------------------------------------------------

MOCK_KPI_ROWS = [
    ["Metric",        "Value"],
    ["Revenue",       "125000"],
    ["New Customers", "342"],
    ["Churn Rate",    "2.3"],
    ["Active Users",  "8750"],
]

# ---------------------------------------------------------------------------
# Helper: parse raw sheet rows → typed KPI dict
# ---------------------------------------------------------------------------

def parse_kpi_rows(rows: list[list[str]]) -> dict:
    """
    Expects rows like [["Metric", "Value"], ["Revenue", "125000"], ...]
    Returns a clean dict: {"revenue": 125000, "new_customers": 342, ...}
    """
    kpis = {}
    for row in rows[1:]:   # skip header
        if len(row) < 2:
            continue
        key   = row[0].strip().lower().replace(" ", "_")   # "New Customers" → "new_customers"
        raw   = row[1].strip()
        # Try numeric conversion
        try:
            value = float(raw) if "." in raw else int(raw)
        except ValueError:
            value = raw
        kpis[key] = value
    return kpis

# ---------------------------------------------------------------------------
# Real Sheets fetch
# ---------------------------------------------------------------------------

def fetch_from_sheets(sheet_name: str) -> dict:
    """Connect to Google Sheets API and read KPI rows."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError:
        logger.error(
            "gspread / google-auth not installed. "
            "Run: pip install gspread google-auth"
        )
        sys.exit(1)

    if not CREDENTIALS_FILE.exists():
        logger.error("Credentials not found at %s", CREDENTIALS_FILE)
        sys.exit(1)

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ]

    creds  = Credentials.from_service_account_file(str(CREDENTIALS_FILE), scopes=scopes)
    client = gspread.authorize(creds)

    logger.info("Connected to Google Sheets API.")
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    try:
        worksheet = spreadsheet.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        logger.error("Sheet tab '%s' not found in spreadsheet.", sheet_name)
        sys.exit(1)

    rows = worksheet.get(DATA_RANGE)
    logger.info("Fetched %d rows from tab '%s'.", len(rows), sheet_name)
    return parse_kpi_rows(rows)

# ---------------------------------------------------------------------------
# Mock fetch (no credentials needed)
# ---------------------------------------------------------------------------

def fetch_mock(sheet_name: str) -> dict:
    """Return simulated KPI data (used with --mock flag)."""
    logger.info("[MOCK] Simulating Sheets fetch for tab '%s'.", sheet_name)
    return parse_kpi_rows(MOCK_KPI_ROWS)

# ---------------------------------------------------------------------------
# Core connector function
# ---------------------------------------------------------------------------

def run_connector(mock: bool = False) -> None:
    """
    1. Read fetch_parameters.json
    2. Fetch KPI data (real or mock)
    3. Write kpi_data.json for Step 4
    """

    # --- 1. Read fetch parameters ------------------------------------------
    if not FETCH_PARAMS_FILE.exists():
        logger.error(
            "fetch_parameters.json not found. "
            "Run 02_processing_function.py first."
        )
        sys.exit(1)

    fetch_params = json.loads(FETCH_PARAMS_FILE.read_text())
    logger.info("Fetch parameters received: %s", fetch_params)

    if fetch_params.get("processing_status") != "ready_to_fetch":
        logger.error(
            "Unexpected processing_status: '%s'. Expected 'ready_to_fetch'.",
            fetch_params.get("processing_status"),
        )
        sys.exit(1)

    sheet_name = fetch_params["sheet_name"]   # e.g. "April 2026"

    # --- 2. Fetch KPI data -------------------------------------------------
    kpis = fetch_mock(sheet_name) if mock else fetch_from_sheets(sheet_name)

    # --- 3. Build output payload -------------------------------------------
    kpi_data = {
        "sheet_name":   sheet_name,
        "fetched_at":   datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "kpis":         kpis,
        "fetch_status": "success",
    }

    # --- 4. Console log (required output) ----------------------------------
    mode_tag = "MOCK" if mock else "SHEETS"
    print(
        f"[SHEETS-{mode_tag}] KPI data fetched for '{sheet_name}'. "
        f"Metrics: {list(kpis.keys())}"
    )

    # --- 5. Structured log -------------------------------------------------
    logger.info("KPI data: %s", kpi_data)

    # --- 6. Persist for Step 4 ---------------------------------------------
    KPI_DATA_FILE.write_text(json.dumps(kpi_data, indent=2))
    logger.info("KPI data saved → %s", KPI_DATA_FILE)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    use_mock = "--mock" in sys.argv
    if use_mock:
        logger.info("--mock flag detected — using simulated Sheets data.")
    run_connector(mock=use_mock)
