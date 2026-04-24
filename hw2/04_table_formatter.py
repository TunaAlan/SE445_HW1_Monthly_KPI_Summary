"""
04_table_formatter.py
=====================
Step 4 — Table Formatter

Reads kpi_data.json produced by Step 3 and formats the raw KPI numbers
into both a plain-text table and an HTML table for email delivery.
Writes email_report.json for Step 5 (Email Sender) to consume.

Usage:
    python 04_table_formatter.py
"""

import json
import logging
from datetime import datetime
from pathlib import Path

BASE_DIR         = Path(__file__).parent
KPI_DATA_FILE    = BASE_DIR / "kpi_data.json"
EMAIL_REPORT_FILE = BASE_DIR / "email_report.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def build_plain_table(sheet_name: str, kpis: dict) -> str:
    lines = [
        f"Monthly KPI Report: {sheet_name}",
        "=" * 40,
        f"{'Metric':<20} {'Value':>10}",
        "-" * 40,
    ]
    for key, value in kpis.items():
        label = key.replace("_", " ").title()
        lines.append(f"{label:<20} {value:>10}")
    lines.append("=" * 40)
    return "\n".join(lines)


def build_html_table(sheet_name: str, kpis: dict) -> str:
    rows = ""
    for key, value in kpis.items():
        label = key.replace("_", " ").title()
        rows += f"<tr><td>{label}</td><td><strong>{value}</strong></td></tr>\n"

    return f"""
<html><body>
<h2>Monthly KPI Report: {sheet_name}</h2>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;">
  <thead>
    <tr style="background:#f2f2f2;">
      <th>Metric</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
{rows}  </tbody>
</table>
</body></html>
""".strip()


def run_formatter() -> None:
    if not KPI_DATA_FILE.exists():
        logger.error("kpi_data.json not found. Run 03_sheets_connector.py first.")
        raise SystemExit(1)

    kpi_data   = json.loads(KPI_DATA_FILE.read_text())
    sheet_name = kpi_data["sheet_name"]
    kpis       = kpi_data["kpis"]

    logger.info("KPI data received for '%s': %s", sheet_name, kpis)

    plain = build_plain_table(sheet_name, kpis)
    html  = build_html_table(sheet_name, kpis)

    print(f"[FORMATTER] Table built for {sheet_name}")
    print(f"\n{plain}\n")

    email_report = {
        "sheet_name":    sheet_name,
        "formatted_at":  datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "subject":       f"Monthly KPI Report: {sheet_name}",
        "plain_body":    plain,
        "html_body":     html,
        "report_status": "ready_to_send",
    }

    EMAIL_REPORT_FILE.write_text(json.dumps(email_report, indent=2))
    logger.info("Email report saved → %s", EMAIL_REPORT_FILE)


if __name__ == "__main__":
    run_formatter()
