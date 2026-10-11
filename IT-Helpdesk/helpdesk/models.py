"""Domain models and schema definitions for HelpDesk Pro."""

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Tuple

VALID_CATEGORIES: Tuple[str, ...] = (
    "Network",
    "Hardware",
    "Software",
    "Access",
    "Email",
    "Other",
)

VALID_PRIORITIES: Tuple[str, ...] = (
    "Low",
    "Medium",
    "High",
    "Critical",
)

VALID_STATUSES: Tuple[str, ...] = (
    "Open",
    "In Progress",
    "Resolved",
    "Closed",
)

REQUIRED_COLUMNS: List[str] = [
    "Ticket ID",
    "Employee name",
    "Category",
    "Priority",
    "Status",
    "Date",
    "Description",
]


@dataclass
class Ticket:
    """Represents a validated IT Helpdesk Ticket."""

    ticket_id: str
    employee_name: str
    category: str
    priority: str
    status: str
    date: str
    description: str

    def to_dict(self) -> Dict[str, str]:
        """Convert Ticket instance to dictionary matching standard column headers."""
        return {
            "Ticket ID": self.ticket_id,
            "Employee name": self.employee_name,
            "Category": self.category,
            "Priority": self.priority,
            "Status": self.status,
            "Date": self.date,
            "Description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Ticket":
        """Create a Ticket instance from a dictionary."""
        return cls(
            ticket_id=str(data.get("Ticket ID", "")).strip(),
            employee_name=str(data.get("Employee name", "")).strip(),
            category=str(data.get("Category", "")).strip(),
            priority=str(data.get("Priority", "")).strip(),
            status=str(data.get("Status", "")).strip(),
            date=str(data.get("Date", "")).strip(),
            description=str(data.get("Description", "")).strip(),
        )


@dataclass
class RejectedRecord:
    """Represents a record rejected during CSV validation with failure reasons."""

    row_number: int
    raw_data: Dict[str, Any]
    reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert rejected record to dictionary representation."""
        return {
            "Row Number": self.row_number,
            "Raw Data": self.raw_data,
            "Reasons": "; ".join(self.reasons),
        }
