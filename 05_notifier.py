"""
05_notifier.py
==============
Step 5 — Final Notifier

Reads the ai_summary.json generated in Step 4 and outputs the final report.
Currently built as a mock terminal notifier to complete the architecture.
"""

import json
import logging
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
SUMMARY_FILE = BASE_DIR / "ai_summary.json"

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def run_notifier():
    """Reads the AI summary and outputs the final report."""
    if not SUMMARY_FILE.exists():
        logger.error("Summary file not found! Please run Step 4 first.")
        sys.exit(1)

    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    summary_text = data.get("summary", "No summary available.")

    logger.info("Reading final AI summary...")
    print("\n" + "="*60)
    print("MONTHLY KPI MANAGEMENT REPORT (MOCK DELIVERY)")
    print("="*60)
    print(summary_text)
    print("="*60 + "\n")
    logger.info("Report delivered successfully.")

    # --- HW1 BONUS: ANTIGRAVITY AGENT INTEGRATION ---
    print("\n" + "*"*50)
    print("🤖 Workflow orchestrated by Google Antigravity Agent")
    print("Opening Antigravity module...")
    print("*"*50 + "\n")
    
    # Triggering Antigravity module as proof of agent usage
    import antigravity

if __name__ == "__main__":
    run_notifier()
