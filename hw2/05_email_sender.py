"""
05_email_sender.py
==================
Step 5 — Email Sender (Gmail SMTP)

Reads email_report.json produced by Step 4 and sends the KPI table
to the configured recipient via Gmail SMTP.

Modes:
    python 05_email_sender.py           # real email delivery
    python 05_email_sender.py --mock    # prints to terminal (no credentials needed)

Requirements:
    pip install python-dotenv

.env variables needed:
    GMAIL_SENDER=your_gmail@gmail.com
    GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx   (Gmail App Password, not regular password)
    EMAIL_RECIPIENT=recipient@example.com
"""

import json
import logging
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR          = Path(__file__).parent
EMAIL_REPORT_FILE = BASE_DIR / "email_report.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def send_email(subject: str, plain_body: str, html_body: str) -> None:
    load_dotenv()
    sender       = os.getenv("GMAIL_SENDER")
    app_password = os.getenv("GMAIL_APP_PASSWORD")
    recipient    = os.getenv("EMAIL_RECIPIENT")

    if not all([sender, app_password, recipient]):
        logger.error(
            "Missing env vars. Set GMAIL_SENDER, GMAIL_APP_PASSWORD, "
            "EMAIL_RECIPIENT in .env"
        )
        sys.exit(1)

    app_password = app_password.replace(" ", "")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = sender
    msg["To"]      = recipient
    msg.attach(MIMEText(plain_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    logger.info("Connecting to Gmail SMTP...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.sendmail(sender, recipient, msg.as_string())

    logger.info("Email sent successfully to %s", recipient)
    print(f"[EMAIL] Report delivered to {recipient}")


def run_sender(mock: bool = False) -> None:
    if not EMAIL_REPORT_FILE.exists():
        logger.error("email_report.json not found. Run 04_table_formatter.py first.")
        sys.exit(1)

    data       = json.loads(EMAIL_REPORT_FILE.read_text())
    subject    = data["subject"]
    plain_body = data["plain_body"]
    html_body  = data["html_body"]
    sheet_name = data["sheet_name"]

    logger.info("Reading email report for '%s'...", sheet_name)

    if mock:
        print("\n" + "=" * 60)
        print(f"MOCK EMAIL — Subject: {subject}")
        print("=" * 60)
        print(plain_body)
        print("=" * 60 + "\n")
        logger.info("Mock email delivery complete.")
    else:
        send_email(subject, plain_body, html_body)


if __name__ == "__main__":
    use_mock = "--mock" in sys.argv
    if use_mock:
        logger.info("--mock flag detected — printing to terminal.")
    run_sender(mock=use_mock)
