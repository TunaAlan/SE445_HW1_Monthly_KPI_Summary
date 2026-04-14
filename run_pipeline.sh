#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "========================================="
echo "Starting Monthly KPI Summary Pipeline"
echo "========================================="

echo -e "\n[1/5] Firing schedule trigger..."
python 01_schedule_trigger.py --now

echo -e "\n[2/5] Processing trigger signal..."
python 02_processing_function.py

echo -e "\n[3/5] Fetching KPI data (Mock Mode)..."
python 03_sheets_connector.py --mock

echo -e "\n[4/5] Generating AI Summary..."
python 04_ai_completion.py

echo -e "\n[5/5] Delivering final report to Slack..."
python 05_notifier.py

echo -e "\n========================================="
echo "Pipeline Execution Completed Successfully!"
echo "========================================="
