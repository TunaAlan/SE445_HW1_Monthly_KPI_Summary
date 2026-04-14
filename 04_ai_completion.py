"""
04_ai_completion.py
===================
Step 4 — AI Completion (Google Gemini)

Reads kpi_data.json produced by Step 3, builds a structured prompt,
calls the Gemini API to generate a management summary, and writes
ai_summary.json for Step 5 (Notifier) to consume.

Modes:
    python 04_ai_completion.py           # real Gemini API call
    python 04_ai_completion.py --mock    # simulated AI response (no API key needed)

Requirements:
    pip install google-genai python-dotenv
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR       = Path(__file__).parent
KPI_DATA_FILE  = BASE_DIR / "kpi_data.json"      # input  (from Step 3)
SUMMARY_FILE   = BASE_DIR / "ai_summary.json"    # output (for Step 5)

GEMINI_MODEL   = "gemini-2.5-flash"              # confirmed available in account

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
# Prompt builder
# ---------------------------------------------------------------------------

def build_prompt(sheet_name: str, kpis: dict) -> str:
    """
    Constructs a structured management-summary prompt from KPI data.
    """
    kpi_lines = "\n".join(
        f"  - {key.replace('_', ' ').title()}: {value}"
        for key, value in kpis.items()
    )
    return f"""You are a business analyst writing a concise monthly KPI summary for senior management.

Here are the KPI results for {sheet_name}:

{kpi_lines}

Write a professional 3-4 sentence executive summary that:
1. Highlights the most important numbers.
2. Notes any areas of concern (e.g. churn rate).
3. Ends with a forward-looking sentence.

Keep it concise and data-driven. Do not use bullet points."""

# ---------------------------------------------------------------------------
# Real Gemini API call
# ---------------------------------------------------------------------------

def call_gemini(prompt: str) -> str:
    """Send prompt to Gemini and return the generated text."""
    try:
        from google import genai
    except ImportError:
        logger.error(
            "google-genai not installed. "
            "Run: pip install google-genai"
        )
        sys.exit(1)

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        logger.error(
            "GEMINI_API_KEY not found. "
            "Make sure it is set in your .env file."
        )
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    logger.info("Calling Gemini API (model: %s)...", GEMINI_MODEL)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )
    return response.text.strip()

# ---------------------------------------------------------------------------
# Mock response (no API key needed)
# ---------------------------------------------------------------------------

def call_mock(sheet_name: str) -> str:
    """Return a static placeholder summary for testing."""
    return (
        f"[MOCK] April 2026 results show strong revenue of $125,000 with 342 new customers "
        f"joining the platform. Active user count stands at 8,750, reflecting healthy engagement. "
        f"Churn rate of 2.3% warrants monitoring to prevent attrition from offsetting growth. "
        f"Looking ahead, sustaining acquisition momentum while addressing churn will be key to "
        f"exceeding Q2 targets."
    )

# ---------------------------------------------------------------------------
# Core AI completion function
# ---------------------------------------------------------------------------

def run_ai_completion(mock: bool = False) -> None:
    """
    1. Read kpi_data.json
    2. Build prompt
    3. Call Gemini (real or mock)
    4. Write ai_summary.json
    """

    # --- 1. Read KPI data --------------------------------------------------
    if not KPI_DATA_FILE.exists():
        logger.error(
            "kpi_data.json not found. "
            "Run 03_sheets_connector.py --mock first."
        )
        sys.exit(1)

    kpi_data   = json.loads(KPI_DATA_FILE.read_text())
    sheet_name = kpi_data["sheet_name"]
    kpis       = kpi_data["kpis"]

    logger.info("KPI data received for '%s': %s", sheet_name, kpis)

    # --- 2. Build prompt ---------------------------------------------------
    prompt = build_prompt(sheet_name, kpis)
    logger.info("Prompt built (%d characters).", len(prompt))

    # --- 3. Generate summary -----------------------------------------------
    if mock:
        logger.info("--mock flag detected — using simulated AI response.")
        summary_text = call_mock(sheet_name)
    else:
        summary_text = call_gemini(prompt)

    # --- 4. Build output payload -------------------------------------------
    ai_summary = {
        "sheet_name":    sheet_name,
        "generated_at":  datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "model":         "mock" if mock else GEMINI_MODEL,
        "summary":       summary_text,
        "summary_status": "ready_to_send",
    }

    # --- 5. Console log (required output) ----------------------------------
    print(f"[AI] Summary generated for {sheet_name}")
    print(f"\n--- SUMMARY ---\n{summary_text}\n---------------\n")

    # --- 6. Structured log -------------------------------------------------
    logger.info("Summary status: %s", ai_summary["summary_status"])

    # --- 7. Persist for Step 5 ---------------------------------------------
    SUMMARY_FILE.write_text(json.dumps(ai_summary, indent=2))
    logger.info("AI summary saved → %s", SUMMARY_FILE)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    use_mock = "--mock" in sys.argv
    run_ai_completion(mock=use_mock)
