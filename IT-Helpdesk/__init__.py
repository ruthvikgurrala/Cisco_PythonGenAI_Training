"""HelpDesk Pro — IT Helpdesk Ticket Management & Analyzer.

Capstone project root package exposing primary domain models, manager,
and analytics entry points.
"""

__version__ = "1.0.0"
__author__ = "HelpDesk Pro Team"

from helpdesk.models import RejectedRecord, Ticket
from helpdesk.ticket_manager import TicketManager
from helpdesk.data_loader import load_tickets_from_csv
from helpdesk.analytics import compute_dashboard_metrics
from helpdesk.report_generator import generate_summary_report

__all__ = [
    "Ticket",
    "RejectedRecord",
    "TicketManager",
    "load_tickets_from_csv",
    "compute_dashboard_metrics",
    "generate_summary_report",
]
