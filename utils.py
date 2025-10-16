import logging
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_current_time_ts() -> float:
    return datetime.now().timestamp()

def get_current_datetime() -> datetime:
    return datetime.now()

def format_remaining_time(remaining_seconds: float) -> str:
    if remaining_seconds < 0:
        remaining_seconds = 0
    
    td = timedelta(seconds=remaining_seconds)
    days, seconds = divmod(td.total_seconds(), 86400)
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds_val = divmod(remainder, 60)
    
    parts = []
    if days > 0:
        parts.append(f"{int(days)} д.")
    if hours > 0 or days > 0:
        parts.append(f"{int(hours)} ч.")
    if minutes > 0 or hours > 0 or days > 0:
         parts.append(f"{int(minutes)} мин.")
    parts.append(f"{int(seconds_val)} сек.")
    
    return " ".join(parts) if parts else "0 сек."