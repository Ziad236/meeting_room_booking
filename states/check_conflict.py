from typing import Dict, Any
from calendar_utils import get_calendar_service, check_availability
from datetime import datetime, timedelta


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check if the user's calendar has a conflict at the requested time.

    Args:
        state (dict): Input state with 'day' and 'time' keys.

    Returns:
        dict: {'user_busy': True/False} or {'error': ...}
    """
    try:
        day = state["day"].lower()
        time_str = state["time"].strip().lower()
        parsed_time = datetime.strptime(time_str, "%I:%M %p")

        now = datetime.utcnow()
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        today_index = now.weekday()
        target_index = days.index(day)
        delta_days = (target_index - today_index) % 7
        target_date = now + timedelta(days=delta_days)

        start_time = target_date.replace(hour=parsed_time.hour, minute=parsed_time.minute, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)

        service = get_calendar_service()
        busy = check_availability(service, start_time, end_time)
        return {"user_busy": bool(busy)}
    except Exception as e:
        return {"error": f"Calendar check failed: {e}"}
