"""Date calculation utilities for IST timezone."""

from datetime import datetime, timedelta
from dateutil import tz
from typing import Tuple


# IST timezone
IST = tz.gettz('Asia/Kolkata')


def get_current_date_ist() -> datetime:
    """Get current date in IST timezone."""
    return datetime.now(IST).replace(hour=0, minute=0, second=0, microsecond=0)


def calculate_days_remaining(end_date_str: str) -> int:
    """
    Calculate days remaining until subscription ends.
    Returns negative number if already expired.

    Args:
        end_date_str: Date string in 'YYYY-MM-DD' format

    Returns:
        Number of days remaining (negative if expired)
    """
    # Parse end date
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    # Get current date in IST
    today = get_current_date_ist().replace(tzinfo=None)

    # Calculate difference
    delta = end_date - today

    return delta.days


def classify_by_expiry(days_remaining: int) -> int:
    """
    Classify subscription into expiry cluster.

    Clusters:
    - 1: Expires in 0-1 days or already expired
    - 3: Expires in 2-3 days
    - 7: Expires in 4-7 days
    - 30: Expires in 8-30 days
    - 0: More than 30 days (skip)

    Args:
        days_remaining: Number of days until expiry

    Returns:
        Cluster number (1, 3, 7, 30, or 0)
    """
    if days_remaining <= 1:
        return 1
    elif days_remaining <= 3:
        return 3
    elif days_remaining <= 7:
        return 7
    elif days_remaining <= 30:
        return 30
    else:
        return 0  # Skip - more than 30 days


def get_expiry_text(days_remaining: int) -> str:
    """
    Get human-readable expiry text.

    Args:
        days_remaining: Number of days until expiry

    Returns:
        Expiry text (e.g., "has expired", "expires today", "expires tomorrow")
    """
    if days_remaining < 0:
        return "has expired"
    elif days_remaining == 0:
        return "expires today"
    elif days_remaining == 1:
        return "expires tomorrow"
    else:
        return f"expires in {days_remaining} days"


def format_date_indian(date_str: str) -> str:
    """
    Format date in Indian format (DD-MM-YYYY).

    Args:
        date_str: Date string in 'YYYY-MM-DD' format

    Returns:
        Date string in 'DD-MM-YYYY' format
    """
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%d-%m-%Y')


def is_leap_year(year: int) -> bool:
    """Check if year is a leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def get_cluster_name(cluster: int) -> str:
    """
    Get display name for cluster.

    Args:
        cluster: Cluster number (1, 3, 7, or 30)

    Returns:
        Display name for cluster
    """
    cluster_names = {
        1: "Urgent (1 day)",
        3: "3 Days",
        7: "7 Days",
        30: "30 Days"
    }
    return cluster_names.get(cluster, "Unknown")


def get_cluster_emoji(cluster: int) -> str:
    """Get emoji for cluster."""
    cluster_emojis = {
        1: "🔴",
        3: "🟡",
        7: "🟢",
        30: "🔵"
    }
    return cluster_emojis.get(cluster, "⚪")
