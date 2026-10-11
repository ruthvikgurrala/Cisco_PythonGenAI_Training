"""Tests for operational analytics and metric calculations."""

import pytest
from helpdesk.analytics import (
    calculate_category_counts,
    calculate_high_and_critical,
    calculate_priority_counts,
    calculate_status_counts,
    compute_dashboard_metrics,
)
from helpdesk.models import Ticket


@pytest.fixture
def analytics_test_tickets():
    return [
        Ticket("T-1", "Emp A", "Network", "Low", "Open", "2026-03-01", "D1"),
        Ticket("T-2", "Emp B", "Network", "Critical", "In Progress", "2026-03-01", "D2"),
        Ticket("T-3", "Emp C", "Hardware", "High", "Resolved", "2026-03-02", "D3"),
        Ticket("T-4", "Emp D", "Software", "Medium", "Closed", "2026-03-02", "D4"),
        Ticket("T-5", "Emp E", "Access", "High", "Open", "2026-03-03", "D5"),
    ]


def test_status_counts(analytics_test_tickets):
    counts = calculate_status_counts(analytics_test_tickets)
    assert counts["Open"] == 2
    assert counts["In Progress"] == 1
    assert counts["Resolved"] == 1
    assert counts["Closed"] == 1


def test_priority_counts(analytics_test_tickets):
    counts = calculate_priority_counts(analytics_test_tickets)
    assert counts["Low"] == 1
    assert counts["Medium"] == 1
    assert counts["High"] == 2
    assert counts["Critical"] == 1


def test_category_counts(analytics_test_tickets):
    counts = calculate_category_counts(analytics_test_tickets)
    assert counts["Network"] == 2
    assert counts["Hardware"] == 1
    assert counts["Software"] == 1
    assert counts["Access"] == 1
    assert counts["Email"] == 0
    assert counts["Other"] == 0


def test_high_and_critical_count(analytics_test_tickets):
    # T-2 (Critical), T-3 (High), T-5 (High) = 3
    assert calculate_high_and_critical(analytics_test_tickets) == 3


def test_compute_dashboard_metrics(analytics_test_tickets):
    metrics = compute_dashboard_metrics(analytics_test_tickets)
    assert metrics["total_tickets"] == 5
    assert metrics["open_tickets"] == 2
    assert metrics["in_progress_tickets"] == 1
    assert metrics["resolved_tickets"] == 1
    assert metrics["closed_tickets"] == 1
    assert metrics["high_and_critical_tickets"] == 3
    # Resolution rate = (1 resolved + 1 closed) / 5 = 40.0%
    assert metrics["resolution_rate_percent"] == 40.0


def test_compute_dashboard_metrics_empty():
    metrics = compute_dashboard_metrics([])
    assert metrics["total_tickets"] == 0
    assert metrics["open_tickets"] == 0
    assert metrics["resolution_rate_percent"] == 0.0
