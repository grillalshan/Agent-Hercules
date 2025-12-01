"""Input validation utilities."""

import re
from datetime import datetime
from typing import Tuple, Optional


def validate_phone_number(phone: str) -> Tuple[bool, str, Optional[str]]:
    """
    Validate and format Indian phone number.
    Returns (is_valid, error_message, formatted_number).
    """
    if not phone:
        return False, "Phone number is empty", None

    # Remove all non-digit characters
    digits = re.sub(r'\D', '', str(phone))

    # Check length
    if len(digits) < 10:
        return False, f"Phone number too short: {phone}", None

    # Take last 10 digits if more than 10
    if len(digits) > 10:
        digits = digits[-10:]

    # Format as +91-XXXXXXXXXX
    formatted = f"+91-{digits}"
    return True, "", formatted


def validate_date_format(date_str: str) -> Tuple[bool, str, Optional[datetime]]:
    """
    Validate date string in DD-MM-YYYY format.
    Returns (is_valid, error_message, datetime_object).
    """
    if not date_str:
        return False, "Date is empty", None

    # Try parsing DD-MM-YYYY
    try:
        # Handle different formats
        date_str = str(date_str).strip()

        # Try DD-MM-YYYY
        try:
            date_obj = datetime.strptime(date_str, "%d-%m-%Y")
            return True, "", date_obj
        except ValueError:
            pass

        # Try DD/MM/YYYY
        try:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y")
            return True, "", date_obj
        except ValueError:
            pass

        # Try YYYY-MM-DD
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return True, "", date_obj
        except ValueError:
            pass

        return False, f"Invalid date format: {date_str}. Expected DD-MM-YYYY", None

    except Exception as e:
        return False, f"Error parsing date: {str(e)}", None


def validate_date_range(start_date: datetime, end_date: datetime) -> Tuple[bool, str]:
    """
    Validate that end_date >= start_date.
    Returns (is_valid, error_message).
    """
    if end_date < start_date:
        return False, "End date cannot be before start date"

    return True, ""


def validate_customer_name(name: str) -> Tuple[bool, str]:
    """
    Validate customer name.
    Returns (is_valid, error_message).
    """
    if not name or not str(name).strip():
        return False, "Customer name is empty"

    # Check for obviously invalid names
    name_str = str(name).strip()
    if len(name_str) < 2:
        return False, "Customer name too short"

    return True, ""


def validate_file_size(file_size: int, max_size_mb: int = 10) -> Tuple[bool, str]:
    """
    Validate file size.
    Returns (is_valid, error_message).
    """
    max_size_bytes = max_size_mb * 1024 * 1024

    if file_size > max_size_bytes:
        actual_size_mb = file_size / (1024 * 1024)
        return False, f"File size ({actual_size_mb:.2f}MB) exceeds {max_size_mb}MB limit"

    return True, ""


def validate_file_extension(filename: str) -> Tuple[bool, str]:
    """
    Validate file extension.
    Returns (is_valid, error_message).
    """
    if not filename:
        return False, "No filename provided"

    allowed_extensions = ['.xlsx', '.xls']
    file_ext = '.' + filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''

    if file_ext not in allowed_extensions:
        return False, f"Invalid file type. Please upload .xlsx or .xls file"

    return True, ""
