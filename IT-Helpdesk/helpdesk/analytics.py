"""Operational analytics and metric calculations for IT helpdesk tickets."""

from typing import Any, Dict, List

from helpdesk.logger import get_logger
from helpdesk.models import (
    VALID_CATEGORIES,
    VALID_PRIORITIES,
    VALID_STATUSES,
    Ticket,
)

logger = get_logger("analytics")


def calculate_status_counts(tickets: List[Ticket]) -> Dict[str, int]:
    """Calculate counts for each standard status."""
    counts = {s: 0 for s in VALID_STATUSES}
    for t in tickets:
        if t.status in counts:
            counts[t.status] += 1
        else:
            counts[t.status] = counts.get(t.status, 0) + 1
    return counts


def calculate_priority_counts(tickets: List[Ticket]) -> Dict[str, int]:
    """Calculate counts for each standard priority."""
    counts = {p: 0 for p in VALID_PRIORITIES}
    for t in tickets:
        if t.priority in counts:
            counts[t.priority] += 1
        else:
            counts[t.priority] = counts.get(t.priority, 0) + 1
    return counts


def calculate_category_counts(tickets: List[Ticket]) -> Dict[str, int]:
    """Calculate counts for each standard category."""
    counts = {c: 0 for c in VALID_CATEGORIES}
    for t in tickets:
        if t.category in counts:
            counts[t.category] += 1
        else:
            counts[t.category] = counts.get(t.category, 0) + 1
    return counts


def calculate_high_and_critical(tickets: List[Ticket]) -> int:
    """Calculate total number of High and Critical priority tickets."""
    return sum(1 for t in tickets if t.priority.lower() in ("high", "critical"))


def compute_dashboard_metrics(tickets: List[Ticket]) -> Dict[str, Any]:
    """Compute complete operational dashboard metrics from actual ticket records."""
    total = len(tickets)
    status_counts = calculate_status_counts(tickets)
    priority_counts = calculate_priority_counts(tickets)
    category_counts = calculate_category_counts(tickets)
    high_critical = calculate_high_and_critical(tickets)

    open_cnt = status_counts.get("Open", 0)
    in_prog_cnt = status_counts.get("In Progress", 0)
    resolved_cnt = status_counts.get("Resolved", 0)
    closed_cnt = status_counts.get("Closed", 0)

    # Resolution rate: (Resolved + Closed) / Total * 100
    resolved_or_closed = resolved_cnt + closed_cnt
    resolution_rate = round((resolved_or_closed / total * 100), 1) if total > 0 else 0.0

    metrics = {
        "total_tickets": total,
        "open_tickets": open_cnt,
        "in_progress_tickets": in_prog_cnt,
        "resolved_tickets": resolved_cnt,
        "closed_tickets": closed_cnt,
        "high_and_critical_tickets": high_critical,
        "resolution_rate_percent": resolution_rate,
        "status_distribution": status_counts,
        "priority_distribution": priority_counts,
        "category_distribution": category_counts,
    }

    logger.debug(
        f"Calculated metrics for {total} tickets: Open={open_cnt}, InProgress={in_prog_cnt}, "
        f"Resolved={resolved_cnt}, Closed={closed_cnt}, High/Critical={high_critical}"
    )
    return metrics
