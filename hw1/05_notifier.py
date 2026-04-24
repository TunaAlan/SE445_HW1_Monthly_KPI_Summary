"""
05_notifier.py
==============
Step 5 — Final Notifier (Slack Integration)

Reads the ai_summary.json generated in Step 4 and sends the final report
to a Slack channel using an Incoming Webhook.

Modes:
    python 05_notifier.py           # real Slack delivery
    python 05_notifier.py --mock    # mock terminal delivery (no credentials needed)

Requirements:
    pip install requests python-dotenv
"""

import json
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent
SUMMARY_FILE = BASE_DIR / "ai_summary.json"

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Core Notifier
# ---------------------------------------------------------------------------

def deliver_to_slack(summary_text: str, sheet_name: str) -> None:
    """Sends the summary to a Slack channel via Webhook."""
    try:
        import requests
    except ImportError:
        logger.error(
            "requests not installed. "
            "Run: pip install requests"
        )
        sys.exit(1)

    load_dotenv()
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        logger.error(
            "SLACK_WEBHOOK_URL not found. "
            "Make sure it is set in your .env file."
        )
        sys.exit(1)

    payload = {
        "text": f"*Monthly KPI Management Report: {sheet_name}*\n\n{summary_text}"
    }

    try:
        logger.info("Sending report to Slack...")
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        logger.info("Slack delivery successful.")
        print(f"[NOTIFIER] Report successfully delivered to Slack for {sheet_name}")
    except requests.exceptions.RequestException as e:
        logger.error("Failed to send message to Slack: %s", e)
        sys.exit(1)

def run_notifier(mock: bool = False) -> None:
    """Reads the AI summary and outputs the final report."""
    if not SUMMARY_FILE.exists():
        logger.error("Summary file not found! Please run Step 4 first.")
        sys.exit(1)

    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    summary_text = data.get("summary", "No summary available.")
    sheet_name = data.get("sheet_name", "Unknown Month")

    logger.info("Reading final AI summary...")
    
    if mock:
        print("\n" + "="*60)
        print(f"MONTHLY KPI MANAGEMENT REPORT: {sheet_name} (MOCK DELIVERY)")
        print("="*60)
        print(summary_text)
        print("="*60 + "\n")
        logger.info("Report delivered successfully. (Mock)")
    else:
        deliver_to_slack(summary_text, sheet_name)

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    use_mock = "--mock" in sys.argv
    if use_mock:
        logger.info("--mock flag detected — using simulated terminal delivery.")
    run_notifier(mock=use_mock)
