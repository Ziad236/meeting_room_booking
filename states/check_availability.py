from services.room_service import has_conflict, get_room_by_name
from typing import Dict, Any


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check if the requested room exists and can accommodate the group size.

    Args:
        state (dict): Input state containing room name, time, day, persons, and parsed flag.

    Returns:
        dict: Availability status, room capacity, and capacity issue flag.
    """
    if not state.get("parsed"):
        return {"error": "Input parsing failed."}

    room = state.get("room")
    day = state.get("day")
    time = state.get("time")
    persons = state.get("persons")

    room_info = get_room_by_name(room)
    if not room_info:
        return {"error": f"Room {room} not found."}

    room_capacity = room_info.get("capacity", 0)

    if persons > room_capacity:
        return {
            "room_available": False,
            "room_capacity": room_capacity,
            "capacity_issue": True
        }

    is_available = not has_conflict(room, day, time)
    return {
        "room_available": is_available,
        "room_capacity": room_capacity,
        "capacity_issue": False
    }
