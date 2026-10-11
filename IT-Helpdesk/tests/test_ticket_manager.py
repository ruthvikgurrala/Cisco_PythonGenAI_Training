"""Tests for TicketManager operations: search, filter, status update, persistence."""

import pytest
from helpdesk.data_loader import load_tickets_from_csv
from helpdesk.models import Ticket
from helpdesk.ticket_manager import TicketManager


@pytest.fixture
def sample_tickets():
    return [
        Ticket(
            ticket_id="TCK-101",
            employee_name="Alice Smith",
            category="Network",
            priority="High",
            status="Open",
            date="2026-03-01",
            description="Wi-Fi unstable",
        ),
        Ticket(
            ticket_id="TCK-102",
            employee_name="Bob Jones",
            category="Hardware",
            priority="Critical",
            status="In Progress",
            date="2026-03-02",
            description="Monitor flickering",
        ),
        Ticket(
            ticket_id="TCK-103",
            employee_name="Alice Wonder",
            category="Software",
            priority="Low",
            status="Resolved",
            date="2026-03-03",
            description="VS Code install",
        ),
        Ticket(
            ticket_id="TCK-104",
            employee_name="Charlie Brown",
            category="Network",
            priority="High",
            status="Closed",
            date="2026-03-04",
            description="Ethernet port issue",
        ),
    ]


def test_view_all_tickets(sample_tickets):
    manager = TicketManager(tickets=sample_tickets)
    assert manager.count == 4
    assert len(manager.tickets) == 4


def test_search_by_ticket_id(sample_tickets):
    manager = TicketManager(tickets=sample_tickets)
    res = manager.search("102")
    assert len(res) == 1
    assert res[0].ticket_id == "TCK-102"


def test_search_by_employee_name(sample_tickets):
    manager = TicketManager(tickets=sample_tickets)
    res = manager.search("alice")
    assert len(res) == 2
    names = [t.employee_name for t in res]
    assert "Alice Smith" in names
    assert "Alice Wonder" in names


def test_filter_by_status(sample_tickets):
    manager = TicketManager(tickets=sample_tickets)
    res = manager.filter_tickets(status="Open")
    assert len(res) == 1
    assert res[0].ticket_id == "TCK-101"


def test_filter_by_priority(sample_tickets):
    manager = TicketManager(tickets=sample_tickets)
    res = manager.filter_tickets(priority="High")
    assert len(res) == 2


def test_filter_by_category(sample_tickets):
    manager = TicketManager(tickets=sample_tickets)
    res = manager.filter_tickets(category="Network")
    assert len(res) == 2


def test_combine_multiple_filters(sample_tickets):
    manager = TicketManager(tickets=sample_tickets)
    # Category = Network AND Status = Closed
    res = manager.filter_tickets(category="Network", status="Closed")
    assert len(res) == 1
    assert res[0].ticket_id == "TCK-104"

    # Search + filters combined
    res2 = manager.query_tickets(query="Brown", category="Network", status="Closed")
    assert len(res2) == 1
    assert res2[0].ticket_id == "TCK-104"


def test_get_ticket_details(sample_tickets):
    manager = TicketManager(tickets=sample_tickets)
    t = manager.get_ticket("TCK-103")
    assert t is not None
    assert t.employee_name == "Alice Wonder"
    assert t.description == "VS Code install"

    assert manager.get_ticket("NON-EXISTENT") is None


def test_valid_status_update(sample_tickets):
    manager = TicketManager(tickets=sample_tickets)
    success, msg = manager.update_status("TCK-101", "In Progress")
    assert success is True
    assert "updated" in msg.lower()
    assert manager.get_ticket("TCK-101").status == "In Progress"


def test_invalid_status_update(sample_tickets):
    manager = TicketManager(tickets=sample_tickets)
    success, msg = manager.update_status("TCK-101", "BogusStatus")
    assert success is False
    assert "invalid status" in msg.lower()
    # Ensure status remained unchanged
    assert manager.get_ticket("TCK-101").status == "Open"


def test_update_nonexistent_ticket(sample_tickets):
    manager = TicketManager(tickets=sample_tickets)
    success, msg = manager.update_status("TCK-999", "Closed")
    assert success is False
    assert "not found" in msg.lower()


def test_persistence_save_and_reload(sample_tickets, tmp_path):
    save_file = tmp_path / "saved_tickets.csv"
    manager = TicketManager(tickets=sample_tickets, filepath=save_file)

    # Update a status
    success, _ = manager.update_status("TCK-101", "Resolved")
    assert success is True

    # Persist
    save_ok, save_msg = manager.save_to_csv()
    assert save_ok is True
    assert save_file.exists()

    # Reload from saved CSV
    reloaded_result = load_tickets_from_csv(save_file)
    assert reloaded_result.is_successful
    assert len(reloaded_result.valid_tickets) == 4

    reloaded_manager = TicketManager(tickets=reloaded_result.valid_tickets)
    updated_ticket = reloaded_manager.get_ticket("TCK-101")
    assert updated_ticket is not None
    assert updated_ticket.status == "Resolved"
