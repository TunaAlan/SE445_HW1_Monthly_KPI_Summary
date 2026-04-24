# SE445 – HW1: Monthly KPI Summary Pipeline

> **Course:** SE445 Prompt Engineering  
> **Assignment:** HW1 – Reporter Setup (Component Foundations)  
> **Author:** Tuna Alan

---

## Project Overview

This project implements an **automated Monthly KPI Summary Pipeline** that:

1. Triggers automatically at the beginning of each month
2. Reads KPI data from a Google Sheets spreadsheet
3. Uses **Google Gemini AI** to generate a professional management summary
4. Delivers the summary as a notification

The pipeline is built in Python using a modular, step-by-step architecture where each component is a standalone script that reads from and writes to a shared JSON signal file.

---

## Required Architecture

```
Trigger → Processing Function → External API (Sheets) → AI Completion
```

| Step | File | Role |
|------|------|------|
| 1 | `01_schedule_trigger.py` | Monthly schedule trigger |
| 2 | `02_processing_function.py` | Signal processor & data mapper |
| 3 | `03_sheets_connector.py` | Google Sheets API connector |
| 4 | `04_ai_completion.py` | Gemini AI summarization |
| 5 | `05_notifier.py` | Sends the final summary as a notification |

---

## File Structure

```
SE445_HW1_Monthly_KPI_Summary/
│
├── 01_schedule_trigger.py      # Step 1 — Monthly trigger (schedule library)
├── 02_processing_function.py   # Step 2 — Signal processor
├── 03_sheets_connector.py      # Step 3 — Google Sheets connector
├── 04_ai_completion.py         # Step 4 — Gemini AI completion
│
├── .env                        # API keys (NOT in git — see .env.example)
├── .env.example                # Template for .env setup
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── workflow_config.json        # Workflow configuration (reserved)
│
└── venv/                       # Python virtual environment (NOT in git)
```

### Runtime-Generated Files (not committed to git)

```
trigger_signal.json             # Output of Step 1 → input of Step 2
fetch_parameters.json           # Output of Step 2 → input of Step 3
kpi_data.json                   # Output of Step 3 → input of Step 4
ai_summary.json                 # Output of Step 4 (final AI summary)
```

---

## Component Details

### Step 1 — Schedule Trigger (`01_schedule_trigger.py`)

Simulates a monthly cron job using the `schedule` library.

- **Trigger time:** 09:00 on the 1st of every month
- **Output:** `trigger_signal.json`

```json
{
  "triggered_at": "2026-04-01T09:00:00",
  "target_month": "2026-04",
  "status": "ready"
}
```

**Console output:**
```
[TRIGGER] Monthly workflow started, passing signal to Processing Function...
```

**Test:**
```bash
python 01_schedule_trigger.py --now   # fires immediately
```

---

### Step 2 — Processing Function (`02_processing_function.py`)

Reads the trigger signal and maps `target_month` to a Google Sheets tab name.

- **Input:** `trigger_signal.json`
- **Output:** `fetch_parameters.json`

```json
{
  "sheet_name": "April 2026",
  "processing_status": "ready_to_fetch"
}
```

**Console output:**
```
[PROCESSOR] Signal processed. Target sheet set to April 2026
```

**Test:**
```bash
python 02_processing_function.py
```

---

### Step 3 — Sheets Connector (`03_sheets_connector.py`)

Connects to Google Sheets and fetches KPI data from the specified monthly tab.

- **Input:** `fetch_parameters.json`
- **Output:** `kpi_data.json`
- **Modes:** Real API (requires credentials) or `--mock` (simulated data)

```json
{
  "sheet_name": "April 2026",
  "fetched_at": "2026-04-01T09:00:05",
  "kpis": {
    "revenue": 125000,
    "new_customers": 342,
    "churn_rate": 2.3,
    "active_users": 8750
  },
  "fetch_status": "success"
}
```

**Console output:**
```
[SHEETS-MOCK] KPI data fetched for 'April 2026'. Metrics: ['revenue', 'new_customers', 'churn_rate', 'active_users']
```

**Test:**
```bash
python 03_sheets_connector.py --mock    # no credentials needed
python 03_sheets_connector.py           # real Google Sheets API
```

---

### Step 4 — AI Completion (`04_ai_completion.py`)

Sends KPI data to **Google Gemini 2.5 Flash** and generates an executive summary.

- **Input:** `kpi_data.json`
- **Output:** `ai_summary.json`
- **Model:** `gemini-2.5-flash`

```json
{
  "sheet_name": "April 2026",
  "generated_at": "2026-04-01T09:00:10",
  "model": "gemini-2.5-flash",
  "summary": "April 2026 demonstrated strong performance...",
  "summary_status": "ready_to_send"
}
```

**Sample AI-generated summary:**
```
April 2026 demonstrated strong performance with revenue reaching 125,000 
and the acquisition of 342 new customers, contributing to a total of 8,750 
active users. However, the churn rate of 2.3% presents an area for focused 
improvement in customer retention efforts. We will prioritize strategies to 
mitigate churn and further capitalize on our user growth in the upcoming period.
```

**Console output:**
```
[AI] Summary generated for April 2026
```

**Test:**
```bash
python 04_ai_completion.py --mock   # simulated response
python 04_ai_completion.py          # real Gemini API
```

---

### Step 5 — Final Notifier (`05_notifier.py`)

Reads the AI summary and sends it as a final report to a Slack channel using an Incoming Webhook, fulfilling the "email/Slack notification integration" requirement.

- **Input:** `ai_summary.json`
- **Output:** Slack Channel Message
- **Integration:** Slack Webhook

**Slack Webhook Setup:**
1. Go to [api.slack.com/apps](https://api.slack.com/apps) and click **Create New App** (From scratch).
2. Enable **Incoming Webhooks**.
3. Click **Add New Webhook to Workspace** and authorize a channel.
4. Copy the Webhook URL and paste it into `.env` as `SLACK_WEBHOOK_URL`.

**Test:**
```bash
python 05_notifier.py --mock   # simulated terminal output (no credentials needed)
python 05_notifier.py          # real Slack delivery (requires .env configuration)
```

---

## Setup & Installation

### Prerequisites

- Python 3.9+
- A Google AI Studio account → [aistudio.google.com](https://aistudio.google.com)

### 1. Clone the repository

```bash
git clone https://github.com/TunaAlan/SE445_HW1_Monthly_KPI_Summary.git
cd SE445_HW1_Monthly_KPI_Summary
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# or: venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
# Edit .env and add your API keys:
# GEMINI_API_KEY=your_gemini_key_here
# SLACK_WEBHOOK_URL=your_slack_webhook_url_here
```

Get your API key from: [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

## Running the Full Pipeline

### Option A: Run the unified orchestrator (Recommended)
This will execute all steps sequentially from start to finish:
```bash
./run_pipeline.sh
```

### Option B: Run steps sequentially manually
```bash
# Step 1 — Fire the trigger
python 01_schedule_trigger.py --now

# Step 2 — Process the signal
python 02_processing_function.py

# Step 3 — Fetch KPI data (mock mode)
python 03_sheets_connector.py --mock

# Step 4 — Generate AI summary
python 04_ai_completion.py

# Step 5 — Deliver to Slack (mock mode)
python 05_notifier.py --mock
```

After all steps, check the final output:
```bash
cat ai_summary.json
```

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `schedule` | 1.2.2 | Monthly trigger simulation |
| `gspread` | 6.1.2 | Google Sheets API |
| `google-auth` | 2.29.0 | Google authentication |
| `google-genai` | ≥0.8.0 | Gemini AI SDK |
| `requests` | >=2.31.0 | Slack Webhook API calls |
| `python-dotenv` | 1.0.1 | Environment variable loading |

---

## Security Notes

- **Never commit `.env`** — it contains your API key
- The `.gitignore` excludes all sensitive and runtime files
- Use `.env.example` as a template when setting up on a new machine
- For Google Sheets real mode, store service account credentials in `credentials/` (also gitignored)

---

## HW1 Grading Criteria Checklist

| Criterion | Points | Status |
|-----------|--------|--------|
| Workflow runs with schedule trigger | 10 | `--now` flag tested |
| GitHub repo is accessible | 10 | public repository |
| Trigger fires & first function receives data | 5 | trigger_signal.json` verified |
| Required architecture implemented | 5 | All 4 components complete |
| **Total** | **30** |

---

## Architecture Diagram

```
┌─────────────────────┐
│  01_schedule_trigger │  ← Fires at 09:00 on the 1st
│  (schedule library)  │
└────────┬────────────┘
         │ trigger_signal.json
         ▼
┌─────────────────────┐
│ 02_processing_       │  ← Maps "2026-04" → "April 2026"
│    function          │
└────────┬────────────┘
         │ fetch_parameters.json
         ▼
┌─────────────────────┐
│ 03_sheets_connector  │  ← Reads KPIs from Google Sheets
│  (Google Sheets API) │     (mock mode available)
└────────┬────────────┘
         │ kpi_data.json
         ▼
┌─────────────────────┐
│ 04_ai_completion     │  ← Gemini 2.5 Flash generates
│  (Google Gemini API) │     executive summary
└────────┬────────────┘
         │ ai_summary.json
         ▼
┌─────────────────────┐
│ 05_notifier         │  ← Delivers final report payload
│  (Slack Webhook)    │     to Slack channel
└────────┬────────────┘
         ▼
    Slack Message
```
