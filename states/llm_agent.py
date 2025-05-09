from services.room_service import get_available_rooms, has_conflict, add_booking
from llm_agent import call_groq_llm
import re

def extract_booking_info(text):
    room_match = re.search(r"room\s*(\d+)", text, re.IGNORECASE)
    time_match = re.search(r"at\s*([\d:]+\s*[APMapm]{2})", text)
    day_match = re.search(r"on\s*(\w+)", text, re.IGNORECASE)
    persons_match = re.search(r"for\s*(\d+)", text)

    return {
        "room": f"Room {room_match.group(1)}" if room_match else None,
        "time": time_match.group(1) if time_match else None,
        "day": day_match.group(1).lower() if day_match else None,
        "persons": int(persons_match.group(1)) if persons_match else None
    }

def run(state):
    user_request = state.get("request", "").lower().strip()

    parsed = extract_booking_info(user_request)
    room = parsed.get("room")
    time = parsed.get("time")
    day = parsed.get("day")
    persons = parsed.get("persons")

    if not all([room, day, time, persons]):
        return {
            "llm_response": (
                "⚠️ I didn't receive complete booking details. Please provide:\n"
                "- Room name\n- Day\n- Time\n- Number of attendees"
            ),
            "room": room,
            "day": day,
            "time": time,
            "persons": persons
        }

    if has_conflict(room, day, time):
        available_rooms = [r for r in get_available_rooms(min_capacity=persons) if r["name"] != room]
        rooms_str = "\n".join([
            f"{r['name']} (Capacity: {r['capacity']}, Features: {r['features']})"
            for r in available_rooms
        ])
        return {
            "llm_response": f"❌ {room} is already booked at {time} on {day}.\n\nAvailable alternatives:\n{rooms_str}",
            "room": room,
            "day": day,
            "time": time,
            "persons": persons
        }

    # ✅ Book immediately if available
    booked = add_booking(room, day, time)
    if booked:
        return {
            "llm_response": f"✅ {room} successfully booked at {time} on {day} for {persons} persons.",
            "room": room,
            "day": day,
            "time": time,
            "persons": persons
        }
    else:
        return {
            "llm_response": "❌ Failed to book the room. Please try again.",
            "room": room,
            "day": day,
            "time": time,
            "persons": persons
        }
