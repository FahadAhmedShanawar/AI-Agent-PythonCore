import re
from datetime import datetime
from typing import List

def parse_date(date_str: str) -> str:
    """Parse various date formats to ISO YYYY-MM-DD"""
    try:
        # Try ISO format first
        datetime.fromisoformat(date_str)
        return date_str
    except ValueError:
        # Try common formats
        for fmt in ['%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
        raise ValueError(f"Unable to parse date: {date_str}")

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount as currency string"""
    return f"{currency} {amount:.2f}"

def clean_description(desc: str) -> str:
    """Clean and normalize description"""
    return desc.strip().lower()

def extract_keywords(desc: str) -> List[str]:
    """Extract keywords from description for categorization"""
    words = re.findall(r'\b\w+\b', desc.lower())
    return [word for word in words if len(word) > 2]
