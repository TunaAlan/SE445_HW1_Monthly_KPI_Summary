"""
02_processing_function.py
=========================
Step 2 — Processing Function

Reads the trigger_signal.json produced by Step 1, validates it,
converts the target_month ("YYYY-MM") to a human-readable Google Sheets
tab name ("Month YYYY"), and writes fetch_parameters.json for Step 3
(the Sheets connector) to consume.

Usage:
    python 02_processing_function.py
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR        = Path(__file__).parent
SIGNAL_FILE     = BASE_DIR / "trigger_signal.json"      # input  (from Step 1)
FETCH_PARAMS    = BASE_DIR / "fetch_parameters.json"    # output (for Step 3)

# ---------------------------------------------------------------------------
# Logging setup  (same format as Step 1 for consistency)
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Helper: "YYYY-MM"  →  "Month YYYY"  (e.g. "2026-04" → "April 2026")
# ---------------------------------------------------------------------------

def month_to_sheet_name(target_month: str) -> str:
    """Convert 'YYYY-MM' string to 'Month YYYY' sheet tab name."""
    dt = datetime.strptime(target_month, "%Y-%m")
    return dt.strftime("%B %Y")   # e.g. "April 2026"

# ---------------------------------------------------------------------------
# Core processing function
# ---------------------------------------------------------------------------

def process_signal() -> None:
    """
    1. Read and validate trigger_signal.json
    2. Map target_month → sheet_name
    3. Write fetch_parameters.json
    4. Log result to console
    """

    # --- 1. Read trigger signal --------------------------------------------
    if not SIGNAL_FILE.exists():
        logger.error(
            "trigger_signal.json not found. "
            "Run 01_schedule_trigger.py --now first."
        )
        sys.exit(1)

    trigger_signal = json.loads(SIGNAL_FILE.read_text())
    logger.info("Trigger signal received: %s", trigger_signal)

    # --- 2. Validate status ------------------------------------------------
    if trigger_signal.get("status") != "ready":
        logger.error(
            "Unexpected signal status: '%s'. Expected 'ready'. Aborting.",
            trigger_signal.get("status"),
        )
        sys.exit(1)

    # --- 3. Map target_month → sheet name ----------------------------------
    target_month = trigger_signal["target_month"]   # e.g. "2026-04"
    sheet_name   = month_to_sheet_name(target_month)  # e.g. "April 2026"

    # --- 4. Build fetch parameters -----------------------------------------
    fetch_parameters = {
        "sheet_name":         sheet_name,
        "processing_status":  "ready_to_fetch",
    }

    # --- 5. Console log (required output) ----------------------------------
    print(
        f"[PROCESSOR] Signal processed. "
        f"Target sheet set to {sheet_name}"
    )

    # --- 6. Structured log -------------------------------------------------
    logger.info("Fetch parameters prepared: %s", fetch_parameters)

    # --- 7. Persist fetch parameters for Step 3 ----------------------------
    FETCH_PARAMS.write_text(json.dumps(fetch_parameters, indent=2))
    logger.info("Fetch parameters saved → %s", FETCH_PARAMS)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    process_signal()
