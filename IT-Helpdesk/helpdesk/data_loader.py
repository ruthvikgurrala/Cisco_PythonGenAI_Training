"""CSV loading and ingestion pipeline with graceful error handling."""

import csv
import io
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, BinaryIO, List, Optional, TextIO, Union

from helpdesk.logger import get_logger
from helpdesk.models import RejectedRecord, Ticket
from helpdesk.validation import validate_headers, validate_ticket_record

logger = get_logger("data_loader")


@dataclass
class DataLoaderResult:
    """Result object of CSV loading and validation process."""

    valid_tickets: List[Ticket] = field(default_factory=list)
    rejected_records: List[RejectedRecord] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    total_rows_processed: int = 0
    source_name: str = ""

    @property
    def is_successful(self) -> bool:
        """True if any valid records were loaded and no fatal file-level errors occurred."""
        return len(self.errors) == 0 and len(self.valid_tickets) > 0


def load_tickets_from_csv(
    source: Union[str, Path, TextIO, BinaryIO],
    source_name: Optional[str] = None,
) -> DataLoaderResult:
    """Load and validate tickets from a CSV file path or file-like buffer.

    Gracefully handles missing files, malformed formatting, and invalid rows.
    """
    result = DataLoaderResult()
    seen_ids = set()

    # Determine file/source name for logging
    if isinstance(source, (str, Path)):
        filepath = Path(source)
        result.source_name = str(filepath)
        logger.info(f"Initiating ticket load from file: {filepath}")

        if not filepath.exists():
            err_msg = f"File not found at path: {filepath}"
            logger.error(err_msg)
            result.errors.append(err_msg)
            return result

        if filepath.stat().st_size == 0:
            err_msg = f"The file '{filepath.name}' is empty (0 bytes)."
            logger.warning(err_msg)
            result.errors.append(err_msg)
            return result

        try:
            with open(filepath, mode="r", encoding="utf-8-sig", newline="") as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(filepath, mode="r", encoding="latin-1", newline="") as f:
                    content = f.read()
            except Exception as e:
                err_msg = f"Failed to decode file '{filepath.name}': {e}"
                logger.error(err_msg)
                result.errors.append(err_msg)
                return result
        except Exception as e:
            err_msg = f"Unexpected error reading file '{filepath.name}': {e}"
            logger.error(err_msg)
            result.errors.append(err_msg)
            return result

    else:
        # File-like object (e.g., Streamlit UploadedFile, StringIO, BytesIO)
        result.source_name = source_name or getattr(source, "name", "StreamBuffer")
        logger.info(f"Loading tickets from stream source: {result.source_name}")
        try:
            if hasattr(source, "getvalue"):
                raw_bytes = source.getvalue()
                if isinstance(raw_bytes, bytes):
                    content = raw_bytes.decode("utf-8-sig", errors="replace")
                else:
                    content = str(raw_bytes)
            elif hasattr(source, "read"):
                read_data = source.read()
                if isinstance(read_data, bytes):
                    content = read_data.decode("utf-8-sig", errors="replace")
                else:
                    content = str(read_data)
            else:
                content = str(source)
        except Exception as e:
            err_msg = f"Failed to read from provided buffer '{result.source_name}': {e}"
            logger.error(err_msg)
            result.errors.append(err_msg)
            return result

    if not content.strip():
        err_msg = f"The source '{result.source_name}' contains no readable data."
        logger.warning(err_msg)
        result.errors.append(err_msg)
        return result

    # Parse CSV content
    reader_stream = io.StringIO(content)
    try:
        csv_reader = csv.DictReader(reader_stream)
        if not csv_reader.fieldnames:
            err_msg = f"CSV has no header row: '{result.source_name}'"
            logger.error(err_msg)
            result.errors.append(err_msg)
            return result

        valid_header, header_errors = validate_headers(csv_reader.fieldnames)
        if not valid_header:
            for err in header_errors:
                logger.error(f"Header validation failure in '{result.source_name}': {err}")
                result.errors.append(err)
            return result

    except csv.Error as e:
        err_msg = f"Malformed CSV structure in '{result.source_name}': {e}"
        logger.error(err_msg)
        result.errors.append(err_msg)
        return result

    # Validate each row
    row_num = 1
    for row in csv_reader:
        row_num += 1
        result.total_rows_processed += 1
        ticket, errors = validate_ticket_record(row, seen_ids=seen_ids, row_number=row_num)
        if ticket:
            result.valid_tickets.append(ticket)
        else:
            logger.warning(
                f"Row {row_num} rejected: {'; '.join(errors)} | Raw data: {dict(row)}"
            )
            result.rejected_records.append(
                RejectedRecord(row_number=row_num, raw_data=dict(row), reasons=errors)
            )

    logger.info(
        f"Completed loading '{result.source_name}': "
        f"{len(result.valid_tickets)} valid records, "
        f"{len(result.rejected_records)} rejected records, "
        f"{len(result.errors)} errors."
    )
    return result
