"""Reporting and data export generation in CSV and JSON formats."""

import csv
import io
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from helpdesk.analytics import compute_dashboard_metrics
from helpdesk.logger import get_logger
from helpdesk.models import REQUIRED_COLUMNS, Ticket

logger = get_logger("report_generator")


def generate_summary_report(tickets: List[Ticket]) -> Dict[str, Any]:
    """Generate structured operational summary report dictionary."""
    metrics = compute_dashboard_metrics(tickets)
    report = {
        "report_metadata": {
            "generated_at": datetime.now().isoformat(),
            "report_title": "HelpDesk Pro - Operational Summary Report",
            "total_records_analyzed": len(tickets),
        },
        "summary_metrics": {
            "total_tickets": metrics["total_tickets"],
            "open_tickets": metrics["open_tickets"],
            "in_progress_tickets": metrics["in_progress_tickets"],
            "resolved_tickets": metrics["resolved_tickets"],
            "closed_tickets": metrics["closed_tickets"],
            "high_and_critical_tickets": metrics["high_and_critical_tickets"],
            "resolution_rate_percent": metrics["resolution_rate_percent"],
        },
        "breakdowns": {
            "by_status": metrics["status_distribution"],
            "by_priority": metrics["priority_distribution"],
            "by_category": metrics["category_distribution"],
        },
    }
    return report


def export_tickets_to_csv(
    tickets: List[Ticket],
    filepath: Optional[Union[str, Path]] = None,
) -> str:
    """Export ticket list to CSV format. Writes to filepath if given, returns CSV string."""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=REQUIRED_COLUMNS)
    writer.writeheader()
    for t in tickets:
        writer.writerow(t.to_dict())

    content = output.getvalue()

    if filepath:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, mode="w", encoding="utf-8", newline="") as f:
            f.write(content)
        logger.info(f"Exported {len(tickets)} tickets to CSV at '{path}'")

    return content


def export_tickets_to_json(
    tickets: List[Ticket],
    filepath: Optional[Union[str, Path]] = None,
    indent: int = 2,
) -> str:
    """Export ticket list to JSON format. Writes to filepath if given, returns JSON string."""
    data = [t.to_dict() for t in tickets]
    content = json.dumps(data, indent=indent, ensure_ascii=False)

    if filepath:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"Exported {len(tickets)} tickets to JSON at '{path}'")

    return content


def export_summary_to_json(
    tickets: List[Ticket],
    filepath: Optional[Union[str, Path]] = None,
    indent: int = 2,
) -> str:
    """Export summary report to JSON format."""
    report = generate_summary_report(tickets)
    content = json.dumps(report, indent=indent, ensure_ascii=False)

    if filepath:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"Exported summary report to JSON at '{path}'")

    return content


def export_summary_to_csv(
    tickets: List[Ticket],
    filepath: Optional[Union[str, Path]] = None,
) -> str:
    """Export operational summary metrics and distributions to a structured CSV format."""
    metrics = compute_dashboard_metrics(tickets)
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Section", "Metric", "Count / Value"])
    writer.writerow(["Overview", "Total Tickets", metrics["total_tickets"]])
    writer.writerow(["Overview", "Open Tickets", metrics["open_tickets"]])
    writer.writerow(["Overview", "In Progress Tickets", metrics["in_progress_tickets"]])
    writer.writerow(["Overview", "Resolved Tickets", metrics["resolved_tickets"]])
    writer.writerow(["Overview", "Closed Tickets", metrics["closed_tickets"]])
    writer.writerow(["Overview", "High & Critical Tickets", metrics["high_and_critical_tickets"]])
    writer.writerow(["Overview", "Resolution Rate (%)", metrics["resolution_rate_percent"]])

    writer.writerow([])
    writer.writerow(["Status Distribution", "Status", "Count"])
    for status, count in metrics["status_distribution"].items():
        writer.writerow(["Status", status, count])

    writer.writerow([])
    writer.writerow(["Priority Distribution", "Priority", "Count"])
    for priority, count in metrics["priority_distribution"].items():
        writer.writerow(["Priority", priority, count])

    writer.writerow([])
    writer.writerow(["Category Distribution", "Category", "Count"])
    for category, count in metrics["category_distribution"].items():
        writer.writerow(["Category", category, count])

    content = output.getvalue()

    if filepath:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, mode="w", encoding="utf-8", newline="") as f:
            f.write(content)
        logger.info(f"Exported summary report to CSV at '{path}'")

    return content
