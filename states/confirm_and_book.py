from typing import Dict, Any
from services.room_service import add_booking


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Finalizes the booking by writing to DB if confirmed.

    Args:
        state (dict): Booking context including confirmed status and room info.

    Returns:
        dict: Confirmation status or error.
    """
    if state.get("confirmed"):
        room = state.get("suggested_room", state.get("room"))
        day = state.get("suggested_day", state.get("day"))
        time = state.get("suggested_time", state.get("time"))

        booked = add_booking(room, day, time)
        if booked:
            return {
                "status": f"✅ Booking confirmed for {room} at {time} on {day}.",
                "room": room,
                "day": day,
                "time": time
            }
        else:
            return {"error": f"❌ Could not confirm booking for {room}. It may be already booked."}

    return {"status": "Waiting for user confirmation..."}
