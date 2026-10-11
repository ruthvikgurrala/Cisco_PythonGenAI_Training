# HelpDesk Pro — IT Helpdesk Ticket Management & Analyzer

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg)](https://streamlit.io/)
[![Pytest](https://img.shields.io/badge/pytest-passing-brightgreen.svg)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**HelpDesk Pro** is a comprehensive, production-grade IT Helpdesk Ticket Management and Operational Analytics application built as a team capstone project for the **Core Python with AI-Integrated Development** course.

---

## 1. Project Overview & Problem Statement

### Problem Statement
Internal IT support departments face common operational friction:
- High ticket volume spanning hardware, network, access, and software requests.
- Fragmented record keeping in flat files or spreadsheets that lack input validation, resulting in duplicate tickets, invalid statuses, and corrupted records.
- Difficulty calculating real-time Key Performance Indicators (KPIs) such as resolution rate, priority backlog, and category distribution.
- Lack of lightweight, zero-configuration local tools to safely update ticket lifecycles without requiring heavy external database deployments or paid third-party APIs.

### Solution & Objectives
**HelpDesk Pro** solves these challenges by providing:
1. **Resilient Data Ingestion:** Validates tickets loaded from CSV, gracefully rejects malformed rows without crashing, and preserves valid records.
2. **Interactive Ticket Management:** Search by ID/Employee, multi-faceted filtering, detail inspection, and validated status lifecycle management.
3. **Atomic Persistence:** Changes are persistently written back to CSV files using atomic swap files to prevent file corruption.
4. **Live Operational Analytics:** Visual dashboard with real-time KPI metrics and breakdown charts computed directly from underlying records.
5. **Multi-Format Export Engine:** Exports operational summaries and ticket datasets into structured CSV and JSON formats.
6. **Centralized Enterprise Logging:** Tracks system events, ingestion errors, search operations, and data mutations to `logs/app.log`.

---

## 2. Key Features

- **📊 Executive Dashboard:**
  - Metric cards for Total Tickets, Open, In Progress, Resolved, Closed, and High/Critical priority.
  - Distribution charts for Status, Priority, and Category using Altair.
  - Live system resolution rate percentage calculation.

- **📋 Ticket Registry & Search:**
  - Case-insensitive substring search by Ticket ID or Employee Name.
  - Multi-criteria filtering by Status, Priority, and Category.
  - Full ticket inspector card with color-coded status badges and detailed issue descriptions.

- **✏️ Ticket Lifecycle Management:**
  - Selection of any ticket and controlled transition between valid lifecycle states (`Open`, `In Progress`, `Resolved`, `Closed`).
  - Validation guards preventing invalid status updates.
  - Atomic persistence to disk ensuring data survives application restarts.

- **📈 Operational Reports & Data Exports:**
  - Executive summary report with metadata, KPI counts, and breakdown dictionaries.
  - Downloadable reports as CSV and JSON.
  - Downloadable filtered ticket datasets as CSV and JSON.

- **🔍 Data Validation Diagnostics:**
  - Real-time audit of total processed rows, valid rows, and rejected rows.
  - Diagnostic breakdown table displaying exact Row Number, Raw Payload, and Failure Reasons.
  - Switchable validation test dataset containing intentional edge-case errors for easy demonstration.

- **📜 Traceable Logging:**
  - Standardized timestamps, severity levels, and module origins written to `logs/app.log`.

---

## 3. Architecture & Design

HelpDesk Pro adheres to strict separation of concerns, ensuring business logic, data models, validation, and analytics are decoupled from the Streamlit UI presentation layer.

```
helpdesk-pro/
├── app.py                      # Streamlit frontend & interactive dashboard
├── helpdesk/                   # Core business logic package
│   ├── __init__.py             # Package exports & metadata
│   ├── models.py               # Ticket & RejectedRecord dataclasses & schema constants
│   ├── validation.py           # Header, date, category, status, priority & duplicate validation
│   ├── data_loader.py          # Resilient CSV parser & stream ingestion pipeline
│   ├── ticket_manager.py       # Querying, filtering, status updates & atomic persistence
│   ├── report_generator.py     # CSV and JSON report & dataset export generation
│   └── logger.py               # Centralized logging configuration
├── data/
│   ├── sample_tickets.csv      # Default clean dataset (25 realistic tickets)
│   ├── error_tickets.csv       # Dedicated error stress dataset (12 validation edge-cases)
│   ├── combined_tickets.csv    # Mixed dataset (25 clean tickets + 12 error tickets)
│   └── malformed_sample.csv    # Compact malformed demonstration dataset
├── logs/
│   ├── .gitkeep
│   └── app.log                 # Runtime application log file
├── reports/
│   └── .gitkeep                # Directory for generated reports
├── tests/                      # Automated unit test suite (39 tests)
│   ├── test_data_loader.py
│   ├── test_validation.py
│   ├── test_ticket_manager.py
│   ├── test_analytics.py
│   └── test_report_generator.py
├── docs/
│   └── AI_ASSISTANCE.md        # AI collaboration, prompts, reviews, and test audit
├── requirements.txt            # Project dependencies
├── pytest.ini                  # Pytest configuration
├── README.md                   # Complete system documentation & execution guide
└── .gitignore                  # Git ignore rules
```

---

### Team Division Structure
- **Teammate 1 (Core Python & Data Management):**
  - Data loading (`data_loader.py`) & schema validation (`validation.py`)
  - Ticket domain models (`models.py`)
  - Search, filtering, status updates, and persistence (`ticket_manager.py`)
  - Unit tests for data loading and ticket management (`test_data_loader.py`, `test_validation.py`, `test_ticket_manager.py`)
- **Teammate 2 (Analytics, Reports & Interface):**
  - KPI & operational metric calculations (`analytics.py`)
  - Multi-format report generation (`report_generator.py`)
  - Streamlit user interface & visualizations (`app.py`)
  - Unit tests for analytics and reports (`test_analytics.py`, `test_report_generator.py`)

---

## 4. Supported Ticket Schema & Constraints

Each ticket record is structured with the following 7 standard columns:

| Column | Type | Constraints / Allowed Values | Description |
|---|---|---|---|
| `Ticket ID` | String | Unique, non-empty (e.g. `TCK-1001`) | Primary identifier for the ticket |
| `Employee name` | String | Non-empty text | Name of the employee requesting support |
| `Category` | String | `Network`, `Hardware`, `Software`, `Access`, `Email`, `Other` | Technical category of issue |
| `Priority` | String | `Low`, `Medium`, `High`, `Critical` | Escalation priority level |
| `Status` | String | `Open`, `In Progress`, `Resolved`, `Closed` | Current lifecycle state |
| `Date` | Date | Valid ISO `YYYY-MM-DD` or standard calendar date | Date ticket was submitted |
| `Description` | String | Non-empty text | Concise description of the issue |

---

## 5. Installation & Setup (Windows PowerShell)

Follow these exact commands to configure the environment and run HelpDesk Pro:

### Step 1: Open PowerShell in Project Root
```powershell
cd "e:\projects\Python training office\IT-Helpdesk"
```

### Step 2: Create and Activate Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

*(Note: If execution of scripts is disabled on your system, enable it for the current session via `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 6. Launching the Application

Start the Streamlit application with:

```powershell
streamlit run app.py
```

Once launched, open your web browser at:
```
http://localhost:8501
```

---

## 7. User Operation Walkthrough

### 1. Navigating the Dashboard
- Open the application and select **📊 Dashboard** from the sidebar.
- Inspect real-time KPI metric cards (Total Tickets, Open, In Progress, Resolved, Closed, Critical/High).
- Review the interactive Altair distribution charts.

### 2. Searching and Inspecting Tickets
- Select **📋 All Tickets** in the sidebar.
- Type an employee name (e.g. `Alice`) or Ticket ID in the search input.
- Use dropdown filters to isolate specific categories, priorities, or statuses.
- Use the **Inspect Ticket Details** dropdown to examine full descriptions, priority tags, and dates.

### 3. Updating Ticket Lifecycle Status
- Select **✏️ Manage Tickets** from the sidebar.
- Choose a ticket from the dropdown.
- Select a new status from the **New Status Target** dropdown (e.g. change `Open` to `In Progress` or `Resolved`).
- Click **💾 Apply & Save Update**.
- Notice the success banner: the update is saved to memory and immediately written to the backing CSV file (`data/sample_tickets.csv`).
- Restart the app or reload the page: the updated status remains intact.

### 4. Exporting Reports and Data
- Select **📈 Reports & Exports** in the sidebar.
- **Operational Summary Report Tab:** Review the generated JSON preview, and click **Download Summary Report (CSV)** or **Download Summary Report (JSON)**.
- **Data Export Center Tab:** Click **Export All Tickets (CSV)** or **Export All Tickets (JSON)** to download the complete ticket roster.

### 5. Demonstrating Data Validation & Malformed Error Handling
- Select **🔍 Data Validation** in the sidebar.
- Under the default dataset, observe: `25 valid records, 0 rejected records`.
- In the sidebar under **Dataset Source**, select **Combined Dataset (25 Valid + 12 Errors)** or **Error-Only Dataset (12 Errors)** and click the load button.
- In the **Data Validation** tab, view the diagnostics table: malformed records are identified with row numbers and exact reasons (e.g., *Invalid category 'AudioVisual'*, *Duplicate Ticket ID*, *Bad calendar date*, *Missing employee name*).
- Switch back to **Default Clean Dataset (25 tickets)** at any time.

---

## 8. Running Automated Tests

Run the complete test suite using `pytest`:

```powershell
.\.venv\Scripts\python -m pytest -v
```

Expected test execution output:
```text
tests/test_analytics.py::test_status_counts PASSED                       [  2%]
tests/test_analytics.py::test_priority_counts PASSED                     [  5%]
tests/test_analytics.py::test_category_counts PASSED                     [  7%]
tests/test_analytics.py::test_high_and_critical_count PASSED             [ 10%]
tests/test_analytics.py::test_compute_dashboard_metrics PASSED           [ 12%]
tests/test_analytics.py::test_compute_dashboard_metrics_empty PASSED     [ 15%]
tests/test_data_loader.py::test_load_sample_tickets_file PASSED          [ 17%]
tests/test_data_loader.py::test_load_missing_file PASSED                 [ 20%]
tests/test_data_loader.py::test_load_empty_file PASSED                   [ 23%]
tests/test_data_loader.py::test_load_missing_required_headers PASSED     [ 25%]
tests/test_data_loader.py::test_load_mixed_valid_and_invalid_records PASSED [ 28%]
tests/test_data_loader.py::test_load_from_in_memory_stream PASSED        [ 30%]
tests/test_data_loader.py::test_load_error_tickets_file PASSED           [ 33%]
tests/test_data_loader.py::test_load_combined_tickets_file PASSED        [ 35%]
tests/test_report_generator.py::test_generate_summary_report PASSED      [ 38%]
tests/test_report_generator.py::test_export_tickets_to_csv PASSED        [ 41%]
tests/test_report_generator.py::test_export_tickets_to_json PASSED       [ 43%]
tests/test_report_generator.py::test_export_summary_to_json PASSED       [ 46%]
tests/test_report_generator.py::test_export_summary_to_csv PASSED        [ 48%]
tests/test_ticket_manager.py::test_view_all_tickets PASSED               [ 51%]
tests/test_ticket_manager.py::test_search_by_ticket_id PASSED            [ 53%]
tests/test_ticket_manager.py::test_search_by_employee_name PASSED        [ 56%]
tests/test_ticket_manager.py::test_filter_by_status PASSED               [ 58%]
tests/test_ticket_manager.py::test_filter_by_priority PASSED             [ 61%]
tests/test_ticket_manager.py::test_filter_by_category PASSED             [ 64%]
tests/test_ticket_manager.py::test_combine_multiple_filters PASSED       [ 66%]
tests/test_ticket_manager.py::test_get_ticket_details PASSED             [ 69%]
tests/test_ticket_manager.py::test_valid_status_update PASSED            [ 71%]
tests/test_ticket_manager.py::test_invalid_status_update PASSED          [ 74%]
tests/test_ticket_manager.py::test_update_nonexistent_ticket PASSED      [ 76%]
tests/test_ticket_manager.py::test_persistence_save_and_reload PASSED    [ 79%]
tests/test_validation.py::test_validate_headers_success PASSED           [ 82%]
tests/test_validation.py::test_validate_headers_missing_column PASSED    [ 84%]
tests/test_validation.py::test_validate_date_formats PASSED              [ 87%]
tests/test_validation.py::test_validate_ticket_record_valid PASSED       [ 89%]
tests/test_validation.py::test_validate_ticket_record_duplicate_id PASSED [ 92%]
tests/test_validation.py::test_validate_ticket_record_invalid_priority_and_status PASSED [ 94%]
tests/test_validation.py::test_validate_ticket_record_invalid_category PASSED [ 97%]
tests/test_validation.py::test_validate_ticket_record_empty_fields PASSED [100%]

============================= 39 passed in 0.74s ==============================
```

---

## 9. Demonstration Screenshot Checklist

During presentations or capstone defense, verify that you have captured or demonstrated:
- [x] **1. Operational Dashboard:** 6 KPI metric cards and 3 distribution charts.
- [x] **2. Ticket Query & Inspection:** Filtered table and single-ticket inspector view.
- [x] **3. Status Update & Persistent Save:** Ticket status transition and success confirmation.
- [x] **4. Report Generation:** Summary JSON structure and CSV/JSON download triggers.
- [x] **5. Data Validation Diagnostics:** Clean dataset confirmation vs. rejected records breakdown on error dataset.
- [x] **6. Application Log Verification:** Inspecting `logs/app.log` to confirm timestamps, events, and update audit trail.

---

## 10. Known Limitations & Future Improvements

### Current Limitations
1. **Concurrency:** Backing storage uses a single CSV file, which is optimal for local desktop tools but not suitable for high-concurrency multi-user write environments.
2. **Authentication:** No employee login or role-based access control (RBAC) is implemented (by design, per capstone requirements).
3. **Attachments:** Tickets do not support file attachments or screenshots.

### Roadmap for Future Releases
- **Database Backend:** Migrate backing storage from CSV to SQLite or PostgreSQL using SQLAlchemy models.
- **Role-Based Access Control:** Add authentication for `Employee` (create & view own tickets) and `IT Agent` (update & resolve).
- **Service Level Agreement (SLA) Tracking:** Add automatic resolution countdown timers based on priority tier (e.g., Critical = 4h, High = 8h).
- **Automated Email Notifications:** Trigger SMTP alerts when ticket status transitions to `Resolved`.
