from datetime import datetime

ALLOWED_PRIORITIES = {"Low", "Medium", "High"}

def sanitize_string(s: str) -> str:
    if s is None:
        return None
    return s.strip()

def parse_priority(value: str) -> str:
    if not value:
        return "Medium"
    v = value.strip().capitalize()
    return v if v in ALLOWED_PRIORITIES else "Medium"

def parse_bool(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).lower() in {"1", "true", "yes", "on"}

def parse_datetime(value):
    if not value:
        return None
    # Accept ISO-like strings: "2025-10-01 15:30:00" or "2025-10-01T15:30:00"
    try:
        return datetime.fromisoformat(value.replace("Z", "").replace("T", " "))
    except Exception:
        return None
