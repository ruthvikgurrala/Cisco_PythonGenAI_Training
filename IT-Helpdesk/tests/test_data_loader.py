"""Tests for data loader functionality and edge cases."""

import io
from pathlib import Path
import pytest

from helpdesk.data_loader import load_tickets_from_csv


def test_load_sample_tickets_file():
    """Verify that the project sample dataset loads with 100% valid records."""
    sample_path = Path("data/sample_tickets.csv")
    assert sample_path.exists(), "Sample CSV file must exist"
    result = load_tickets_from_csv(sample_path)
    assert result.is_successful
    assert len(result.valid_tickets) >= 20
    assert len(result.rejected_records) == 0
    assert len(result.errors) == 0


def test_load_missing_file(tmp_path):
    """Graceful handling of non-existent CSV file."""
    fake_path = tmp_path / "non_existent.csv"
    result = load_tickets_from_csv(fake_path)
    assert not result.is_successful
    assert len(result.valid_tickets) == 0
    assert len(result.errors) == 1
    assert "File not found" in result.errors[0]


def test_load_empty_file(tmp_path):
    """Graceful handling of empty 0-byte file."""
    empty_path = tmp_path / "empty.csv"
    empty_path.write_text("", encoding="utf-8")
    result = load_tickets_from_csv(empty_path)
    assert not result.is_successful
    assert len(result.valid_tickets) == 0
    assert any("empty" in e.lower() for e in result.errors)


def test_load_missing_required_headers(tmp_path):
    """Handle CSV missing critical columns."""
    bad_header_path = tmp_path / "bad_headers.csv"
    bad_header_path.write_text(
        "Ticket ID,Employee name,Category\nTCK-001,John Doe,Software\n",
        encoding="utf-8",
    )
    result = load_tickets_from_csv(bad_header_path)
    assert not result.is_successful
    assert len(result.valid_tickets) == 0
    assert any("Missing required column" in e for e in result.errors)


def test_load_mixed_valid_and_invalid_records(tmp_path):
    """Ensure invalid rows are rejected while valid rows are preserved."""
    csv_content = """Ticket ID,Employee name,Category,Priority,Status,Date,Description
TCK-201,Alice,Network,High,Open,2026-03-01,Valid ticket 1
TCK-202,Bob,Hardware,SuperUrgent,Open,2026-03-01,Invalid priority
TCK-203,Charlie,Software,Low,PendingState,2026-03-02,Invalid status
TCK-204,Diana,Access,Medium,Closed,2026-03-02,Valid ticket 2
TCK-204,DuplicateDiana,Access,Medium,Closed,2026-03-02,Duplicate ticket ID
"""
    test_file = tmp_path / "mixed.csv"
    test_file.write_text(csv_content, encoding="utf-8")

    result = load_tickets_from_csv(test_file)
    assert len(result.valid_tickets) == 2
    assert len(result.rejected_records) == 3
    assert result.total_rows_processed == 5

    valid_ids = [t.ticket_id for t in result.valid_tickets]
    assert "TCK-201" in valid_ids
    assert "TCK-204" in valid_ids

    # Check rejection reasons
    rejections = {r.raw_data.get("Ticket ID"): r.reasons for r in result.rejected_records}
    assert any("Invalid priority" in r for r in rejections.get("TCK-202", []))
    assert any("Invalid status" in r for r in rejections.get("TCK-203", []))
    assert any("Duplicate Ticket ID" in r for r in rejections.get("TCK-204", []))


def test_load_from_in_memory_stream():
    """Verify loading from file-like stream (such as Streamlit upload)."""
    stream_content = """Ticket ID,Employee name,Category,Priority,Status,Date,Description
TCK-301,Eva,Email,Medium,Open,2026-03-05,Outlook won't sync
"""
    buf = io.StringIO(stream_content)
    result = load_tickets_from_csv(buf, source_name="UploadedBuffer.csv")
    assert result.is_successful
    assert len(result.valid_tickets) == 1
    assert result.valid_tickets[0].ticket_id == "TCK-301"


def test_load_error_tickets_file():
    """Verify that error_tickets.csv correctly flags all 12 malformed rows."""
    error_path = Path("data/error_tickets.csv")
    assert error_path.exists(), "error_tickets.csv must exist"
    result = load_tickets_from_csv(error_path)
    assert len(result.valid_tickets) == 0
    assert len(result.rejected_records) == 12


def test_load_combined_tickets_file():
    """Verify that combined_tickets.csv preserves 25 valid tickets while rejecting all 12 malformed rows."""
    combined_path = Path("data/combined_tickets.csv")
    assert combined_path.exists(), "combined_tickets.csv must exist"
    result = load_tickets_from_csv(combined_path)
    assert len(result.valid_tickets) == 25
    assert len(result.rejected_records) == 12
    assert result.total_rows_processed == 37

