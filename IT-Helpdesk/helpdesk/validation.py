"""Validation rules and checking logic for IT helpdesk tickets."""

from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from helpdesk.models import (
    REQUIRED_COLUMNS,
    VALID_CATEGORIES,
    VALID_PRIORITIES,
    VALID_STATUSES,
    Ticket,
)

# Canonical mapping for case-insensitive validation
_CATEGORY_MAP = {c.lower(): c for c in VALID_CATEGORIES}
_PRIORITY_MAP = {p.lower(): p for p in VALID_PRIORITIES}
_STATUS_MAP = {s.lower(): s for s in VALID_STATUSES}

DATE_FORMATS = [
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%d-%m-%Y",
    "%d/%m/%Y",
    "%m/%d/%Y",
]


def parse_and_validate_date(date_str: str) -> Optional[str]:
    """Validate date string and return normalized ISO format YYYY-MM-DD, or None if invalid."""
    if not date_str:
        return None
    cleaned = date_str.strip()
    for fmt in DATE_FORMATS:
        try:
            parsed = datetime.strptime(cleaned, fmt)
            # Basic sanity check on year range (e.g., between 2000 and 2100)
            if 2000 <= parsed.year <= 2100:
                return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def validate_headers(headers: List[str]) -> Tuple[bool, List[str]]:
    """Validate that all required columns are present in headers."""
    header_clean = [h.strip() for h in headers if h is not None]
    missing = [col for col in REQUIRED_COLUMNS if col not in header_clean]
    if missing:
        return False, [f"Missing required column(s): {', '.join(missing)}"]
    return True, []


def validate_ticket_record(
    row: Dict[str, Any],
    seen_ids: Set[str],
    row_number: int = 1,
) -> Tuple[Optional[Ticket], List[str]]:
    """Validate a single ticket row dictionary.

    Returns:
        (Ticket, []) if valid, or (None, list_of_error_reasons) if invalid.
    """
    errors: List[str] = []

    # 1. Check required fields for non-emptiness
    cleaned_data: Dict[str, str] = {}
    for col in REQUIRED_COLUMNS:
        val = row.get(col)
        val_str = "" if val is None else str(val).strip()
        if not val_str:
            errors.append(f"Field '{col}' cannot be empty")
        cleaned_data[col] = val_str

    ticket_id = cleaned_data.get("Ticket ID", "")
    emp_name = cleaned_data.get("Employee name", "")
    cat_raw = cleaned_data.get("Category", "")
    pri_raw = cleaned_data.get("Priority", "")
    stat_raw = cleaned_data.get("Status", "")
    date_raw = cleaned_data.get("Date", "")
    desc = cleaned_data.get("Description", "")

    # 2. Duplicate Ticket ID check
    if ticket_id:
        if ticket_id in seen_ids:
            errors.append(f"Duplicate Ticket ID '{ticket_id}' detected")
        else:
            seen_ids.add(ticket_id)

    # 3. Category validation
    canonical_cat = _CATEGORY_MAP.get(cat_raw.lower()) if cat_raw else None
    if cat_raw and not canonical_cat:
        errors.append(
            f"Invalid category '{cat_raw}'. Allowed categories: {', '.join(VALID_CATEGORIES)}"
        )

    # 4. Priority validation
    canonical_pri = _PRIORITY_MAP.get(pri_raw.lower()) if pri_raw else None
    if pri_raw and not canonical_pri:
        errors.append(
            f"Invalid priority '{pri_raw}'. Allowed priorities: {', '.join(VALID_PRIORITIES)}"
        )

    # 5. Status validation
    canonical_stat = _STATUS_MAP.get(stat_raw.lower()) if stat_raw else None
    if stat_raw and not canonical_stat:
        errors.append(
            f"Invalid status '{stat_raw}'. Allowed statuses: {', '.join(VALID_STATUSES)}"
        )

    # 6. Date validation
    normalized_date = parse_and_validate_date(date_raw) if date_raw else None
    if date_raw and not normalized_date:
        errors.append(
            f"Invalid date format or value '{date_raw}'. Expected YYYY-MM-DD or standard calendar date"
        )

    if errors:
        return None, errors

    ticket = Ticket(
        ticket_id=ticket_id,
        employee_name=emp_name,
        category=canonical_cat or cat_raw,
        priority=canonical_pri or pri_raw,
        status=canonical_stat or stat_raw,
        date=normalized_date or date_raw,
        description=desc,
    )
    return ticket, []
