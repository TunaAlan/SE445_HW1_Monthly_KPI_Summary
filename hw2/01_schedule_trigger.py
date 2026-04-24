"""
01_schedule_trigger.py
======================
Step 1 — Monthly Schedule Trigger

Simulates a monthly cron-style trigger using the `schedule` library.
Fires at 09:00 on the 1st of every month, generates a trigger_signal,
logs to console, and saves the signal to a JSON file for the next step.

Usage:
    python 01_schedule_trigger.py            # runs the scheduler loop
    python 01_schedule_trigger.py --now      # fires immediately (for testing)
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import schedule
import time

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent
SIGNAL_FILE = BASE_DIR / "trigger_signal.json"

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
# Core trigger function
# ---------------------------------------------------------------------------


def monthly_trigger() -> None:
    """
    Called at 09:00 on the 1st of the month (or immediately in --now mode).
    Builds the trigger_signal, logs it, and persists it to JSON.
    """
    now = datetime.now()

    # Only act when it is actually the 1st — schedule fires daily at 09:00,
    # so we guard against non-1st days here.
    if not os.environ.get("TRIGGER_FORCE") and now.day != 1:
        logger.debug("Today is not the 1st — skipping trigger.")
        return

    triggered_at = now.strftime("%Y-%m-%dT%H:%M:%S")
    target_month = now.strftime("%Y-%m")

    trigger_signal: dict = {
        "triggered_at": triggered_at,
        "target_month": target_month,
        "status": "ready",
    }

    # --- Console log (required output) -------------------------------------
    print(
        "[TRIGGER] Monthly workflow started, "
        "passing signal to Processing Function..."
    )

    # --- Structured log ----------------------------------------------------
    logger.info("Trigger signal created: %s", trigger_signal)

    # --- Persist to JSON ---------------------------------------------------
    SIGNAL_FILE.write_text(json.dumps(trigger_signal, indent=2))
    logger.info("Trigger signal saved → %s", SIGNAL_FILE)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    # --now flag: fire once immediately (useful for testing / CI)
    if "--now" in sys.argv:
        logger.info("--now flag detected — firing trigger immediately.")
        os.environ["TRIGGER_FORCE"] = "1"   # bypass day-of-month guard
        monthly_trigger()
        return

    # Normal mode: schedule for 09:00 every day; monthly_trigger() self-guards
    # for the 1st of the month.
    logger.info("Scheduler started — trigger is set for 09:00 on the 1st of each month.")
    schedule.every().day.at("09:00").do(monthly_trigger)

    try:
        while True:
            schedule.run_pending()
            time.sleep(30)   # check every 30 seconds
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user.")


if __name__ == "__main__":
    main()
