"""HelpDesk Pro - IT Helpdesk Ticket Management & Analyzer.

Streamlit web application providing operational dashboards, ticket search & filtering,
status lifecycle management, reporting exports, and data validation diagnostics.
"""

from pathlib import Path
from typing import Optional
import json

import altair as alt
import pandas as pd
import streamlit as st

from helpdesk.analytics import compute_dashboard_metrics
from helpdesk.data_loader import DataLoaderResult, load_tickets_from_csv
from helpdesk.logger import get_logger
from helpdesk.models import (
    REQUIRED_COLUMNS,
    VALID_CATEGORIES,
    VALID_PRIORITIES,
    VALID_STATUSES,
    Ticket,
)
from helpdesk.report_generator import (
    export_summary_to_csv,
    export_summary_to_json,
    export_tickets_to_csv,
    export_tickets_to_json,
    generate_summary_report,
)
from helpdesk.ticket_manager import TicketManager

# Configure root logger
logger = get_logger("app")

# Page configuration
st.set_page_config(
    page_title="HelpDesk Pro | IT Ticket Management & Analyzer",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling for polished, professional IT Support UI
CUSTOM_CSS = """
<style>
    /* Metric Card Styling */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px 20px;
        color: #f8fafc;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .metric-title {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.9rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.1;
    }
    .metric-sub {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 6px;
    }

    /* Status Badges */
    .badge {
        display: inline-block;
        padding: 3px 8px;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 9999px;
    }
    .badge-open { background-color: #0284c7; color: white; }
    .badge-progress { background-color: #d97706; color: white; }
    .badge-resolved { background-color: #16a34a; color: white; }
    .badge-closed { background-color: #475569; color: white; }
    .badge-critical { background-color: #dc2626; color: white; }
    .badge-high { background-color: #ea580c; color: white; }
    .badge-med { background-color: #2563eb; color: white; }
    .badge-low { background-color: #64748b; color: white; }

    /* Detail Inspector Box */
    .detail-container {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 20px;
        margin-top: 10px;
        color: #f1f5f9;
    }
    .detail-label {
        font-weight: 600;
        color: #94a3b8;
        font-size: 0.85rem;
        text-transform: uppercase;
    }
    .detail-value {
        font-size: 1.05rem;
        color: #f8fafc;
        margin-bottom: 12px;
    }
    .detail-desc {
        background-color: #1e293b;
        border-left: 4px solid #38bdf8;
        padding: 12px 16px;
        border-radius: 4px;
        font-size: 0.95rem;
        line-height: 1.5;
        color: #e2e8f0;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


DEFAULT_CSV_PATH = Path("data/sample_tickets.csv")
MALFORMED_CSV_PATH = Path("data/malformed_sample.csv")
ERROR_CSV_PATH = Path("data/error_tickets.csv")
COMBINED_CSV_PATH = Path("data/combined_tickets.csv")


def initialize_session_state() -> None:
    """Initialize session state holding ticket manager and load results."""
    if "ticket_manager" not in st.session_state:
        logger.info("Initializing new application session state")
        result = load_tickets_from_csv(DEFAULT_CSV_PATH)
        st.session_state.load_result = result
        st.session_state.current_source = str(DEFAULT_CSV_PATH)
        st.session_state.ticket_manager = TicketManager(
            tickets=result.valid_tickets,
            filepath=DEFAULT_CSV_PATH,
        )


initialize_session_state()
mgr: TicketManager = st.session_state.ticket_manager
load_result: DataLoaderResult = st.session_state.load_result


# --- SIDEBAR: Navigation & Data Source ---
with st.sidebar:
    st.markdown("### 🛠️ HelpDesk Pro")
    st.caption("IT Support Operations & Diagnostics")
    st.markdown("---")

    navigation = st.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "📋 All Tickets",
            "✏️ Manage Tickets",
            "📈 Reports & Exports",
            "🔍 Data Validation",
            "ℹ️ About",
        ],
        index=0,
    )

    st.markdown("---")
    st.subheader("Data Source")

    source_options = [
        "Default Clean Dataset (25 tickets)",
        "Combined Dataset (25 Valid + 12 Errors)",
        "Error-Only Dataset (12 Errors)",
        "Malformed Sample (6 Errors)",
        "Upload Custom CSV",
    ]

    current_selection_idx = 0
    if st.session_state.current_source == str(COMBINED_CSV_PATH):
        current_selection_idx = 1
    elif st.session_state.current_source == str(ERROR_CSV_PATH):
        current_selection_idx = 2
    elif st.session_state.current_source == str(MALFORMED_CSV_PATH):
        current_selection_idx = 3
    elif st.session_state.current_source != str(DEFAULT_CSV_PATH):
        current_selection_idx = 4

    source_mode = st.radio(
        "Dataset Source",
        source_options,
        index=current_selection_idx,
    )

    def _switch_dataset(target_path: Path, label: str) -> None:
        if st.session_state.current_source != str(target_path):
            if st.button(f"Load {label}"):
                res = load_tickets_from_csv(target_path)
                st.session_state.load_result = res
                st.session_state.current_source = str(target_path)
                mgr.set_tickets(res.valid_tickets, filepath=target_path)
                logger.info(f"Switched to {label}")
                st.rerun()

    if source_mode == "Default Clean Dataset (25 tickets)":
        _switch_dataset(DEFAULT_CSV_PATH, "Clean Dataset")

    elif source_mode == "Combined Dataset (25 Valid + 12 Errors)":
        _switch_dataset(COMBINED_CSV_PATH, "Combined Dataset")

    elif source_mode == "Error-Only Dataset (12 Errors)":
        _switch_dataset(ERROR_CSV_PATH, "Error-Only Dataset")

    elif source_mode == "Malformed Sample (6 Errors)":
        _switch_dataset(MALFORMED_CSV_PATH, "Malformed Sample")

    else:
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
        if uploaded_file is not None:
            if st.button("Ingest Uploaded File"):
                res = load_tickets_from_csv(uploaded_file, source_name=uploaded_file.name)
                st.session_state.load_result = res
                st.session_state.current_source = uploaded_file.name
                mgr.set_tickets(res.valid_tickets, filepath=None)
                logger.info(f"Ingested uploaded dataset: {uploaded_file.name}")
                st.rerun()

    st.markdown("---")
    st.markdown(
        f"**Active Source:** `{Path(st.session_state.current_source).name}`  \n"
        f"**Active Tickets:** `{mgr.count}` valid records"
    )
    if st.button("🔄 Reset / Reload Data"):
        res = load_tickets_from_csv(DEFAULT_CSV_PATH)
        st.session_state.load_result = res
        st.session_state.current_source = str(DEFAULT_CSV_PATH)
        mgr.set_tickets(res.valid_tickets, filepath=DEFAULT_CSV_PATH)
        logger.info("User requested data reset")
        st.success("Dataset successfully reloaded!")
        st.rerun()


# =========================================================================
# 1. DASHBOARD
# =========================================================================
if navigation == "📊 Dashboard":
    st.header("Operational Dashboard", divider="blue")
    st.caption("Live metrics calculated in real-time from active ticket records.")

    all_tickets = mgr.tickets
    metrics = compute_dashboard_metrics(all_tickets)

    # Metric Cards Row
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-title">Total Tickets</div>
                <div class="metric-value">{metrics['total_tickets']}</div>
                <div class="metric-sub">Across all categories</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-title" style="color:#38bdf8;">Open</div>
                <div class="metric-value">{metrics['open_tickets']}</div>
                <div class="metric-sub">Awaiting assignment</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-title" style="color:#fbbf24;">In Progress</div>
                <div class="metric-value">{metrics['in_progress_tickets']}</div>
                <div class="metric-sub">Under active diagnosis</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-title" style="color:#4ade80;">Resolved</div>
                <div class="metric-value">{metrics['resolved_tickets']}</div>
                <div class="metric-sub">Fix implemented</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c5:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-title" style="color:#94a3b8;">Closed</div>
                <div class="metric-value">{metrics['closed_tickets']}</div>
                <div class="metric-sub">Confirmed finalized</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c6:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-title" style="color:#f87171;">Critical / High</div>
                <div class="metric-value">{metrics['high_and_critical_tickets']}</div>
                <div class="metric-sub">Priority escalation</div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts Row
    ch1, ch2, ch3 = st.columns(3)

    # 1. Status Chart
    with ch1:
        st.subheader("Tickets by Status")
        status_df = pd.DataFrame(
            [{"Status": k, "Count": v} for k, v in metrics["status_distribution"].items()]
        )
        chart_status = (
            alt.Chart(status_df)
            .mark_bar(cornerRadius=6)
            .encode(
                x=alt.X("Status:N", sort=list(VALID_STATUSES), title="Status"),
                y=alt.Y("Count:Q", title="Number of Tickets"),
                color=alt.Color(
                    "Status:N",
                    scale=alt.Scale(
                        domain=["Open", "In Progress", "Resolved", "Closed"],
                        range=["#0284c7", "#d97706", "#16a34a", "#64748b"],
                    ),
                    legend=None,
                ),
                tooltip=["Status", "Count"],
            )
            .properties(height=280)
        )
        st.altair_chart(chart_status, use_container_width=True)

    # 2. Priority Chart
    with ch2:
        st.subheader("Tickets by Priority")
        priority_df = pd.DataFrame(
            [{"Priority": k, "Count": v} for k, v in metrics["priority_distribution"].items()]
        )
        chart_priority = (
            alt.Chart(priority_df)
            .mark_bar(cornerRadius=6)
            .encode(
                x=alt.X("Priority:N", sort=list(VALID_PRIORITIES), title="Priority"),
                y=alt.Y("Count:Q", title="Number of Tickets"),
                color=alt.Color(
                    "Priority:N",
                    scale=alt.Scale(
                        domain=["Low", "Medium", "High", "Critical"],
                        range=["#64748b", "#3b82f6", "#ea580c", "#ef4444"],
                    ),
                    legend=None,
                ),
                tooltip=["Priority", "Count"],
            )
            .properties(height=280)
        )
        st.altair_chart(chart_priority, use_container_width=True)

    # 3. Category Chart
    with ch3:
        st.subheader("Tickets by Category")
        category_df = pd.DataFrame(
            [{"Category": k, "Count": v} for k, v in metrics["category_distribution"].items()]
        )
        chart_category = (
            alt.Chart(category_df)
            .mark_bar(cornerRadius=6)
            .encode(
                y=alt.Y("Category:N", sort="-x", title="Category"),
                x=alt.X("Count:Q", title="Number of Tickets"),
                color=alt.Color(
                    "Category:N",
                    scale=alt.Scale(scheme="tableau10"),
                    legend=None,
                ),
                tooltip=["Category", "Count"],
            )
            .properties(height=280)
        )
        st.altair_chart(chart_category, use_container_width=True)

    # Additional Insight Strip
    st.markdown("---")
    st.markdown(
        f"**System Resolution Rate:** `{metrics['resolution_rate_percent']}%` of all tickets have reached Resolved or Closed status."
    )


# =========================================================================
# 2. ALL TICKETS (SEARCH, FILTER & DETAILS)
# =========================================================================
elif navigation == "📋 All Tickets":
    st.header("Ticket Registry & Inspection", divider="blue")
    st.caption("Browse, query, filter, and inspect detailed IT support records.")

    # Search & Filter Controls
    fc1, fc2, fc3, fc4 = st.columns([2, 1, 1, 1])
    with fc1:
        search_query = st.text_input(
            "🔍 Search Ticket ID or Employee Name",
            placeholder="e.g. TCK-1002 or Alice...",
            help="Case-insensitive substring search",
        )
    with fc2:
        status_filter = st.selectbox(
            "Status Filter",
            options=["All"] + list(VALID_STATUSES),
            index=0,
        )
    with fc3:
        priority_filter = st.selectbox(
            "Priority Filter",
            options=["All"] + list(VALID_PRIORITIES),
            index=0,
        )
    with fc4:
        category_filter = st.selectbox(
            "Category Filter",
            options=["All"] + list(VALID_CATEGORIES),
            index=0,
        )

    # Query execution
    filtered_tickets = mgr.query_tickets(
        query=search_query,
        status=status_filter,
        priority=priority_filter,
        category=category_filter,
    )

    st.markdown(
        f"Showing **{len(filtered_tickets)}** of **{mgr.count}** tickets matching current criteria."
    )

    if filtered_tickets:
        df = mgr.to_dataframe(filtered_tickets)

        # Interactive Table
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Ticket ID": st.column_config.TextColumn("Ticket ID", width="small"),
                "Employee name": st.column_config.TextColumn("Employee Name", width="medium"),
                "Category": st.column_config.TextColumn("Category", width="small"),
                "Priority": st.column_config.TextColumn("Priority", width="small"),
                "Status": st.column_config.TextColumn("Status", width="small"),
                "Date": st.column_config.DateColumn("Date", width="small"),
                "Description": st.column_config.TextColumn("Description", width="large"),
            },
        )

        st.markdown("---")
        st.subheader("Inspect Ticket Details")

        ticket_options = [f"{t.ticket_id} - {t.employee_name} ({t.category})" for t in filtered_tickets]
        selected_option = st.selectbox("Select a ticket to inspect:", ticket_options)

        if selected_option:
            selected_id = selected_option.split(" - ")[0].strip()
            ticket = mgr.get_ticket(selected_id)
            if ticket:
                # Custom details presentation
                dc1, dc2, dc3, dc4 = st.columns(4)
                with dc1:
                    st.markdown("**Ticket ID:**")
                    st.code(ticket.ticket_id)
                with dc2:
                    st.markdown("**Employee:**")
                    st.write(ticket.employee_name)
                with dc3:
                    st.markdown("**Category:**")
                    st.write(ticket.category)
                with dc4:
                    st.markdown("**Date Logged:**")
                    st.write(ticket.date)

                dc5, dc6 = st.columns(2)
                with dc5:
                    st.markdown("**Current Priority:**")
                    pri_color = {
                        "Critical": "badge-critical",
                        "High": "badge-high",
                        "Medium": "badge-med",
                        "Low": "badge-low",
                    }.get(ticket.priority, "badge-low")
                    st.markdown(
                        f'<span class="badge {pri_color}">{ticket.priority}</span>',
                        unsafe_allow_html=True,
                    )
                with dc6:
                    st.markdown("**Current Status:**")
                    stat_color = {
                        "Open": "badge-open",
                        "In Progress": "badge-progress",
                        "Resolved": "badge-resolved",
                        "Closed": "badge-closed",
                    }.get(ticket.status, "badge-closed")
                    st.markdown(
                        f'<span class="badge {stat_color}">{ticket.status}</span>',
                        unsafe_allow_html=True,
                    )

                st.markdown("**Full Issue Description:**")
                st.markdown(
                    f'<div class="detail-desc">{ticket.description}</div>',
                    unsafe_allow_html=True,
                )
    else:
        st.warning("No tickets match the selected search or filter criteria.")


# =========================================================================
# 3. MANAGE TICKETS (STATUS LIFECYCLE & PERSISTENCE)
# =========================================================================
elif navigation == "✏️ Manage Tickets":
    st.header("Ticket Status Management", divider="blue")
    st.caption("Update ticket lifecycle status with validation and atomic persistent save.")

    all_tickets = mgr.tickets
    if not all_tickets:
        st.warning("No tickets available to manage.")
    else:
        ticket_map = {f"{t.ticket_id} | {t.employee_name} [{t.status}]": t.ticket_id for t in all_tickets}
        selected_display = st.selectbox(
            "Select Ticket to Update:",
            list(ticket_map.keys()),
        )
        selected_id = ticket_map[selected_display]
        ticket = mgr.get_ticket(selected_id)

        if ticket:
            st.markdown("---")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Ticket ID", ticket.ticket_id)
            m2.metric("Employee", ticket.employee_name)
            m3.metric("Category", ticket.category)
            m4.metric("Current Status", ticket.status)

            st.info(f"**Issue Summary:** {ticket.description}")

            st.markdown("#### Change Status")
            current_status_idx = (
                list(VALID_STATUSES).index(ticket.status)
                if ticket.status in VALID_STATUSES
                else 0
            )

            col_form, col_save = st.columns([2, 1])
            with col_form:
                new_status = st.selectbox(
                    "New Status Target",
                    options=list(VALID_STATUSES),
                    index=current_status_idx,
                )

            with col_save:
                st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
                update_btn = st.button("💾 Apply & Save Update", type="primary", use_container_width=True)

            if update_btn:
                if new_status == ticket.status:
                    st.info(f"Ticket {ticket.ticket_id} is already in status '{ticket.status}'. No change required.")
                else:
                    success, msg = mgr.update_status(ticket.ticket_id, new_status)
                    if success:
                        # Persist to disk if file path exists
                        if mgr.filepath:
                            save_ok, save_msg = mgr.save_to_csv()
                            if save_ok:
                                logger.info(f"Saved status change to {mgr.filepath}")
                                st.success(f"{msg} and permanently saved to `{mgr.filepath.name}`.")
                            else:
                                st.error(f"{msg}, but persistence failed: {save_msg}")
                        else:
                            st.warning(f"{msg} (in memory only, since uploaded file had no fixed disk path).")
                        st.rerun()
                    else:
                        st.error(f"Update failed: {msg}")


# =========================================================================
# 4. REPORTS & EXPORTS
# =========================================================================
elif navigation == "📈 Reports & Exports":
    st.header("Operational Reports & Data Exports", divider="blue")
    st.caption("Generate structured metrics and export raw or filtered ticket data in CSV and JSON formats.")

    all_tickets = mgr.tickets
    summary_report = generate_summary_report(all_tickets)
    metrics = summary_report["summary_metrics"]

    t1, t2 = st.tabs(["📊 Operational Summary Report", "💾 Data Export Center"])

    with t1:
        st.subheader("Executive Metrics Overview")
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Total Analyzed", metrics["total_tickets"])
        r2.metric("Active Backlog (Open + In Progress)", metrics["open_tickets"] + metrics["in_progress_tickets"])
        r3.metric("Resolved & Closed", metrics["resolved_tickets"] + metrics["closed_tickets"])
        r4.metric("Resolution Rate", f"{metrics['resolution_rate_percent']}%")

        st.markdown("#### Structured Summary JSON")
        st.json(summary_report)

        col_rep1, col_rep2 = st.columns(2)
        with col_rep1:
            csv_summary_str = export_summary_to_csv(all_tickets)
            st.download_button(
                label="📥 Download Summary Report (CSV)",
                data=csv_summary_str,
                file_name="helpdesk_summary_report.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with col_rep2:
            json_summary_str = export_summary_to_json(all_tickets)
            st.download_button(
                label="📥 Download Summary Report (JSON)",
                data=json_summary_str,
                file_name="helpdesk_summary_report.json",
                mime="application/json",
                use_container_width=True,
            )

    with t2:
        st.subheader("Export Ticket Records")
        st.caption("Download current ticket records as standard CSV or JSON.")

        ec1, ec2 = st.columns(2)
        with ec1:
            tickets_csv = export_tickets_to_csv(all_tickets)
            st.download_button(
                label="📥 Export All Tickets (CSV)",
                data=tickets_csv,
                file_name="helpdesk_tickets_export.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with ec2:
            tickets_json = export_tickets_to_json(all_tickets)
            st.download_button(
                label="📥 Export All Tickets (JSON)",
                data=tickets_json,
                file_name="helpdesk_tickets_export.json",
                mime="application/json",
                use_container_width=True,
            )


# =========================================================================
# 5. DATA VALIDATION DIAGNOSTICS
# =========================================================================
elif navigation == "🔍 Data Validation":
    st.header("Data Validation & Diagnostics", divider="blue")
    st.caption("Health report of ingested CSV data, schema compliance, and rejected records breakdown.")

    res = st.session_state.load_result

    v1, v2, v3 = st.columns(3)
    v1.metric("Total Records Processed", res.total_rows_processed)
    v2.metric("Valid Records Ingested", len(res.valid_tickets))
    v3.metric("Rejected Records", len(res.rejected_records))

    if res.errors:
        st.error("File-Level Ingestion Errors:")
        for err in res.errors:
            st.write(f"- ❌ {err}")

    if res.rejected_records:
        st.subheader("Rejected Records Diagnostics")
        st.warning(f"{len(res.rejected_records)} row(s) failed validation checks and were excluded from active processing.")

        rejections_data = [r.to_dict() for r in res.rejected_records]
        rejections_df = pd.DataFrame(rejections_data)
        st.dataframe(rejections_df, use_container_width=True)
    else:
        st.success("✅ Clean dataset: All records met all schema constraints with 0 validation rejections!")

    st.markdown("---")
    st.subheader("Validation Rules Reference")
    st.markdown(
        """
        - **Required Columns:** `Ticket ID`, `Employee name`, `Category`, `Priority`, `Status`, `Date`, `Description`.
        - **Empty Values:** All required fields must contain non-whitespace text.
        - **Allowed Categories:** `Network`, `Hardware`, `Software`, `Access`, `Email`, `Other`.
        - **Allowed Priorities:** `Low`, `Medium`, `High`, `Critical`.
        - **Allowed Statuses:** `Open`, `In Progress`, `Resolved`, `Closed`.
        - **Date Formats:** Standard ISO `YYYY-MM-DD` and common calendar variations.
        - **Unique IDs:** Duplicate `Ticket ID` entries within the dataset are detected and rejected.
        """
    )


# =========================================================================
# 6. ABOUT
# =========================================================================
elif navigation == "ℹ️ About":
    st.header("About HelpDesk Pro", divider="blue")
    st.markdown(
        """
        ### System Overview
        **HelpDesk Pro** is an IT Helpdesk Ticket Management & Analyzer application built as a capstone project
        for the *Core Python with AI-Integrated Development* course.

        The system models a lightweight internal IT support operations tool designed to streamline incident triage,
        monitor service delivery KPIs, and safely manage ticket status lifecycles.

        ---

        ### Key Capabilities
        - **Robust CSV Ingestion & Validation:** Handles malformed files, schema mismatches, duplicate IDs, and invalid field values gracefully without crashing.
        - **Search & Multi-Facet Filtering:** Rapidly isolate tickets by Employee Name, Ticket ID, Category, Priority, and Status.
        - **Persistent Lifecycle Management:** Update ticket statuses with immediate persistence directly to backing CSV storage.
        - **Operational Metrics Dashboard:** Live calculation of resolution rates, priority distribution, category workloads, and status queues.
        - **Multi-Format Export Engine:** Export operational reports and ticket datasets to CSV and JSON formats.
        - **Traceable Enterprise Logging:** Centralized logging with timestamps and log levels stored at `logs/app.log`.

        ---

        ### Technology Stack
        - **Core Language:** Python 3.11+
        - **Interface:** Streamlit 1.35+
        - **Data Processing:** Pandas, Altair
        - **Testing:** Pytest test suite (37 unit tests covering models, validation, loader, manager, analytics, exports)
        - **Logging:** Python native `logging` module

        ---

        ### Team Division & Architecture
        - **Teammate 1 (Core Python & Data Management):** Data loading, schema validation, domain models, search/filtering, status lifecycle updates, and persistence.
        - **Teammate 2 (Analytics, Reports & Streamlit Interface):** Metric computation, operational dashboards, report generation, UI/UX workflow integration, and export controls.
        """
    )
