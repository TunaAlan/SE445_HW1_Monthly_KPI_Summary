SE445 Homework & Final Project Guidelines
1. Important Deadlines & Submission
Please upload all homework assignments and your final project to Moodle.

HW1 due: April 14, 2026

HW2 due: April 24, 2026

HW3 due: May 6, 2026

Final Project submission: May 12, 2026

Final Project presentation: June 2, 2026

2. Tools & Bonus Points
Main Environment: All work is expected to be done in Google Antigravity (agents + workflows).

Alternative: If you prefer, you may use n8n instead. (You may build everything using prompts in Antigravity, preferably, or n8n).

Bonus 1: Students who use Antigravity receive a +5 bonus in advance.

Bonus 2: Weekly Lab activities introduce up to +5 bonus points as well.

3. Project Topic & Groups
Group Size: Form groups of ideally 5-6 students.

Topic Selection: Pick one of the given project types (Lead capture, Customer support triage, Social content repurposer, etc.).

Rule: Each group must have a unique topic (first-come, first-served).

Action: Inform the instructor of your project subject and group members as soon as possible.

Alignment: Your Final Project and all 3 Homeworks will be aligned with this chosen topic.

4. Common Rules for All Homeworks & Final Project
You must be able to do the following during your presentations:

Understand your workflow (Live Demo):

Walk through each step of your workflow in real time.

You cannot just read from the screen; you must show understanding and explain what each step does.

Document clearly:

Describe main files, endpoints, and nodes and their purposes in your own words.

Show at least one test case:

For each homework assignment and for the final project, you must demonstrate at least one full test run.

5. Deliverables Summary
5.1. For each Homework (HW1, HW2, HW3)
Submit:

GitHub repository link (must be public or accessible).

Required code, configuration, and artifacts (workflows, exports, etc.).

Short Word report explaining:

How your solution meets the HW requirements.

How the workflow is structured (triggers, steps, outputs).

5.2. For the Final Project
Submit:

GitHub project page link.

Source code and configuration.

Word report including:

Overall design, architecture, and data flow.

Prompts and AI logic.

Data schema (fields, storage, integrations).

Group live demo during presentation week.

6. Grading Rubric & Required Architecture
6.1. HW1 – Component Foundations (30%)
Check (10 points): Workflow runs with the specified trigger (HTTP, form, schedule). Initial script/configuration starts correctly.

Deliverable check (10 points): GitHub repo is public or accessible. Primary logic file is present.

Success criteria (5 points): Trigger fires, and the first function receives data correctly.

Required architecture (5 points): Trigger (Form/Webhook/Schedule) → Processing Function → External API (Sheets/CRM) → AI Completion.

6.2. HW2 – Data Input & Persistence (30%)
Check (10 points): Sending a test payload to the endpoint. Data appears correctly in the destination (Google Sheet / CRM).

Deliverable check (10 points): Word report includes a screenshot or proof of successful data entry.

Success criteria (5 points): No data loss. No formatting errors during transfer.

Required architecture (5 points): HTTP POST Request ({name, email, message}) → Antigravity Connector → Google Sheets / CRM.

7. Project Topic Details: 5. Monthly KPI Summary
(If this is your chosen topic, follow these specific instructions for your assignments)

Business case: Generate an AI-written management summary from raw metrics and deliver it automatically.

HW1: Reporter Setup (Learn components)

Create a monthly schedule-like trigger (e.g., a monthly workflow).

Connect it to a spreadsheet or database to read KPI data.

Set up an AI summarization function.

Integrate an email/Slack notification.

HW2: Raw Data Export (First results)

Pull raw numbers (revenue, new customers, churn, etc.) from a single sheet.

Send an automated email that lists these raw numbers in a simple table or bullet list.

HW3: Growth Analysis

Use AI to write a narrative report based on the numbers.

Calculate if the numbers went up or down compared to last month, and include this in the prompt.