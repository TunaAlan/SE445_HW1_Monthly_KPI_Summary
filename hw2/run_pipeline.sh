#!/bin/bash
set -e

echo "========================================="
echo "Starting HW2 — Raw Data Export Pipeline"
echo "========================================="

echo -e "\n[1/5] Firing schedule trigger..."
python 01_schedule_trigger.py --now

echo -e "\n[2/5] Processing trigger signal..."
python 02_processing_function.py

echo -e "\n[3/5] Fetching KPI data from Google Sheets..."
python 03_sheets_connector.py

echo -e "\n[4/5] Formatting KPI data as table..."
python 04_table_formatter.py

echo -e "\n[5/5] Sending email report..."
python 05_email_sender.py

echo -e "\n========================================="
echo "Pipeline Execution Completed Successfully!"
echo "========================================="
