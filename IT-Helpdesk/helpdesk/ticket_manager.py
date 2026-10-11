"""Ticket manager orchestrating search, filtering, status updates, and persistent storage."""

import csv
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import pandas as pd

from helpdesk.logger import get_logger
from helpdesk.models import (
    REQUIRED_COLUMNS,
    VALID_STATUSES,
    Ticket,
)

logger = get_logger("ticket_manager")


class TicketManager:
    """Manages IT Helpdesk tickets, search, filter, updates, and persistence."""

    def __init__(
        self,
        tickets: Optional[List[Ticket]] = None,
        filepath: Optional[Union[str, Path]] = None,
    ):
        self._tickets: List[Ticket] = list(tickets) if tickets else []
        self._filepath: Optional[Path] = Path(filepath) if filepath else None

    @property
    def tickets(self) -> List[Ticket]:
        """Return the current list of tickets."""
        return list(self._tickets)

    @property
    def count(self) -> int:
        """Total number of tickets managed."""
        return len(self._tickets)

    @property
    def filepath(self) -> Optional[Path]:
        """Current backing CSV file path."""
        return self._filepath

    @filepath.setter
    def filepath(self, path: Union[str, Path]) -> None:
        self._filepath = Path(path)

    def set_tickets(self, tickets: List[Ticket], filepath: Optional[Union[str, Path]] = None) -> None:
        """Replace internal tickets list and optionally update filepath."""
        self._tickets = list(tickets)
        if filepath is not None:
            self._filepath = Path(filepath)
        logger.info(f"Loaded {len(self._tickets)} tickets into TicketManager")

    def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        """Retrieve a ticket by its Ticket ID (case-insensitive)."""
        target_id = ticket_id.strip().lower()
        for t in self._tickets:
            if t.ticket_id.lower() == target_id:
                return t
        return None

    def search(
        self,
        query: str,
        tickets: Optional[List[Ticket]] = None,
    ) -> List[Ticket]:
        """Search tickets by ticket ID or employee name (case-insensitive substring)."""
        source = self._tickets if tickets is None else tickets
        q = query.strip().lower()
        if not q:
            return list(source)

        matched = [
            t for t in source
            if q in t.ticket_id.lower() or q in t.employee_name.lower()
        ]
        logger.debug(f"Search query '{query}' matched {len(matched)} of {len(source)} tickets")
        return matched

    def filter_tickets(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category: Optional[str] = None,
        tickets: Optional[List[Ticket]] = None,
    ) -> List[Ticket]:
        """Filter tickets by status, priority, and/or category.

        Can combine multiple filters simultaneously.
        """
        results = self._tickets if tickets is None else tickets

        if status and status.strip() and status != "All":
            s_clean = status.strip().lower()
            results = [t for t in results if t.status.lower() == s_clean]

        if priority and priority.strip() and priority != "All":
            p_clean = priority.strip().lower()
            results = [t for t in results if t.priority.lower() == p_clean]

        if category and category.strip() and category != "All":
            c_clean = category.strip().lower()
            results = [t for t in results if t.category.lower() == c_clean]

        return results

    def query_tickets(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category: Optional[str] = None,
    ) -> List[Ticket]:
        """Combine search and multi-criteria filtering in a single call."""
        filtered = self.filter_tickets(status=status, priority=priority, category=category)
        if query and query.strip():
            filtered = self.search(query=query, tickets=filtered)
        return filtered

    def update_status(self, ticket_id: str, new_status: str) -> Tuple[bool, str]:
        """Update ticket status with strict validation.

        Returns (success: bool, message: str).
        """
        if not ticket_id or not ticket_id.strip():
            msg = "Ticket ID cannot be empty."
            logger.warning(f"Update rejected: {msg}")
            return False, msg

        ticket = self.get_ticket(ticket_id)
        if not ticket:
            msg = f"Ticket '{ticket_id}' not found."
            logger.warning(f"Update rejected: {msg}")
            return False, msg

        # Validate status against allowed values
        canonical_map = {s.lower(): s for s in VALID_STATUSES}
        matched_status = canonical_map.get(new_status.strip().lower())

        if not matched_status:
            msg = f"Invalid status '{new_status}'. Allowed statuses: {', '.join(VALID_STATUSES)}."
            logger.warning(f"Update rejected for {ticket_id}: {msg}")
            return False, msg

        old_status = ticket.status
        ticket.status = matched_status
        msg = f"Ticket {ticket.ticket_id} status updated from '{old_status}' to '{ticket.status}'."
        logger.info(msg)
        return True, msg

    def save_to_csv(self, target_path: Optional[Union[str, Path]] = None) -> Tuple[bool, str]:
        """Persistently save all current tickets to CSV file.

        Does not silently discard existing records.
        """
        dest_path = Path(target_path) if target_path else self._filepath
        if not dest_path:
            msg = "No file path specified to save tickets."
            logger.error(msg)
            return False, msg

        try:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            # Write to a temporary file first then replace to avoid corruption
            temp_path = dest_path.with_suffix(".tmp")
            with open(temp_path, mode="w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS)
                writer.writeheader()
                for ticket in self._tickets:
                    writer.writerow(ticket.to_dict())

            temp_path.replace(dest_path)
            self._filepath = dest_path
            msg = f"Successfully persisted {len(self._tickets)} tickets to '{dest_path}'."
            logger.info(msg)
            return True, msg
        except Exception as e:
            msg = f"Failed to persist tickets to '{dest_path}': {e}"
            logger.error(msg)
            return False, msg

    def to_dataframe(self, tickets: Optional[List[Ticket]] = None) -> pd.DataFrame:
        """Convert list of tickets (or all tickets) to a pandas DataFrame."""
        source = self._tickets if tickets is None else tickets
        if not source:
            return pd.DataFrame(columns=REQUIRED_COLUMNS)
        data = [t.to_dict() for t in source]
        return pd.DataFrame(data)
