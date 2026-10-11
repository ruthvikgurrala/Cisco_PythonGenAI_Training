"""Tests for reporting and data export functions."""

import json
from pathlib import Path
import pytest

from helpdesk.models import Ticket
from helpdesk.report_generator import (
    export_summary_to_csv,
    export_summary_to_json,
    export_tickets_to_csv,
    export_tickets_to_json,
    generate_summary_report,
)


@pytest.fixture
def reporting_test_tickets():
    return [
        Ticket("TCK-01", "Alice", "Network", "High", "Open", "2026-03-01", "Wi-Fi"),
        Ticket("TCK-02", "Bob", "Hardware", "Low", "Resolved", "2026-03-02", "Mouse"),
    ]


def test_generate_summary_report(reporting_test_tickets):
    report = generate_summary_report(reporting_test_tickets)
    assert "report_metadata" in report
    assert "summary_metrics" in report
    assert "breakdowns" in report
    assert report["summary_metrics"]["total_tickets"] == 2
    assert report["summary_metrics"]["open_tickets"] == 1
    assert report["summary_metrics"]["resolved_tickets"] == 1


def test_export_tickets_to_csv(reporting_test_tickets, tmp_path):
    out_file = tmp_path / "exported_tickets.csv"
    csv_str = export_tickets_to_csv(reporting_test_tickets, filepath=out_file)

    assert "Ticket ID" in csv_str
    assert "TCK-01" in csv_str
    assert "TCK-02" in csv_str
    assert out_file.exists()

    content = out_file.read_text(encoding="utf-8")
    lines = content.strip().splitlines()
    assert len(lines) == 3  # Header + 2 rows


def test_export_tickets_to_json(reporting_test_tickets, tmp_path):
    out_file = tmp_path / "exported_tickets.json"
    json_str = export_tickets_to_json(reporting_test_tickets, filepath=out_file)

    parsed = json.loads(json_str)
    assert isinstance(parsed, list)
    assert len(parsed) == 2
    assert parsed[0]["Ticket ID"] == "TCK-01"
    assert out_file.exists()


def test_export_summary_to_json(reporting_test_tickets, tmp_path):
    out_file = tmp_path / "summary.json"
    json_str = export_summary_to_json(reporting_test_tickets, filepath=out_file)

    parsed = json.loads(json_str)
    assert parsed["summary_metrics"]["total_tickets"] == 2
    assert out_file.exists()


def test_export_summary_to_csv(reporting_test_tickets, tmp_path):
    out_file = tmp_path / "summary.csv"
    csv_str = export_summary_to_csv(reporting_test_tickets, filepath=out_file)

    assert "Overview" in csv_str
    assert "Status Distribution" in csv_str
    assert "Priority Distribution" in csv_str
    assert out_file.exists()
