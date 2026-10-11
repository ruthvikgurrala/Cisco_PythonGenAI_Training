"""Tests for ticket data validation rules."""

import pytest
from helpdesk.validation import (
    parse_and_validate_date,
    validate_headers,
    validate_ticket_record,
)
from helpdesk.models import REQUIRED_COLUMNS


def test_validate_headers_success():
    headers = [
        "Ticket ID",
        "Employee name",
        "Category",
        "Priority",
        "Status",
        "Date",
        "Description",
    ]
    valid, errors = validate_headers(headers)
    assert valid is True
    assert len(errors) == 0


def test_validate_headers_missing_column():
    headers = ["Ticket ID", "Employee name", "Category", "Priority", "Status"]
    valid, errors = validate_headers(headers)
    assert valid is False
    assert any("Date" in e for e in errors)
    assert any("Description" in e for e in errors)


def test_validate_date_formats():
    assert parse_and_validate_date("2026-03-01") == "2026-03-01"
    assert parse_and_validate_date("2026/03/01") == "2026-03-01"
    assert parse_and_validate_date("01-03-2026") == "2026-03-01"
    assert parse_and_validate_date("invalid-date") is None
    assert parse_and_validate_date("") is None
    assert parse_and_validate_date(None) is None


def test_validate_ticket_record_valid():
    row = {
        "Ticket ID": "TCK-101",
        "Employee name": "John Doe",
        "Category": "Network",
        "Priority": "High",
        "Status": "Open",
        "Date": "2026-03-10",
        "Description": "Wi-Fi down",
    }
    seen = set()
    ticket, errors = validate_ticket_record(row, seen_ids=seen, row_number=2)
    assert ticket is not None
    assert errors == []
    assert ticket.ticket_id == "TCK-101"
    assert "TCK-101" in seen


def test_validate_ticket_record_duplicate_id():
    row1 = {
        "Ticket ID": "TCK-101",
        "Employee name": "John Doe",
        "Category": "Network",
        "Priority": "High",
        "Status": "Open",
        "Date": "2026-03-10",
        "Description": "Wi-Fi down",
    }
    seen = set()
    t1, err1 = validate_ticket_record(row1, seen_ids=seen, row_number=2)
    assert t1 is not None

    # Second row with same ID
    row2 = dict(row1)
    row2["Employee name"] = "Jane Doe"
    t2, err2 = validate_ticket_record(row2, seen_ids=seen, row_number=3)
    assert t2 is None
    assert any("Duplicate Ticket ID" in e for e in err2)


def test_validate_ticket_record_invalid_priority_and_status():
    row = {
        "Ticket ID": "TCK-102",
        "Employee name": "Alice",
        "Category": "Software",
        "Priority": "UrgentNow",  # Invalid
        "Status": "PendingReview",  # Invalid
        "Date": "2026-03-10",
        "Description": "Crash bug",
    }
    seen = set()
    ticket, errors = validate_ticket_record(row, seen_ids=seen, row_number=2)
    assert ticket is None
    assert any("Invalid priority" in e for e in errors)
    assert any("Invalid status" in e for e in errors)


def test_validate_ticket_record_invalid_category():
    row = {
        "Ticket ID": "TCK-103",
        "Employee name": "Bob",
        "Category": "SecurityInfrastructure",  # Invalid
        "Priority": "Low",
        "Status": "Closed",
        "Date": "2026-03-10",
        "Description": "General inquiry",
    }
    seen = set()
    ticket, errors = validate_ticket_record(row, seen_ids=seen, row_number=2)
    assert ticket is None
    assert any("Invalid category" in e for e in errors)


def test_validate_ticket_record_empty_fields():
    row = {
        "Ticket ID": "",
        "Employee name": "   ",
        "Category": "Hardware",
        "Priority": "Medium",
        "Status": "Open",
        "Date": "2026-03-10",
        "Description": "",
    }
    seen = set()
    ticket, errors = validate_ticket_record(row, seen_ids=seen, row_number=2)
    assert ticket is None
    assert any("Ticket ID" in e for e in errors)
    assert any("Employee name" in e for e in errors)
    assert any("Description" in e for e in errors)
