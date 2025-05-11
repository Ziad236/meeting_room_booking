from services.room_service import get_available_rooms
from llm_agent import call_groq_llm
import re

def run(state):
    room = state.get("room")
    time = state.get("time")
    day = state.get("day")
    persons = state.get("persons")
    room_available = state.get("room_available")
    user_busy = state.get("user_busy")
    room_capacity = state.get("room_capacity", "?")
    capacity_issue = state.get("capacity_issue", False)

    available_rooms = get_available_rooms(min_capacity=persons)
    rooms_str = "\n".join([
        f"{r['name']} (Capacity: {r['capacity']}, Features: {r['features']})"
        for r in available_rooms
    ]) or "None found."

    prompt = f"""
You are an AI assistant helping users book meeting rooms.

User request:
- Room: {room}
- Time: {time}
- Day: {day}
- Group size: {persons}

Room info:
- Capacity: {room_capacity}
- Capacity issue: {"yes" if capacity_issue else "no"}
- Room availability: {"available" if room_available else "booked"}
- User calendar status: {"free" if not user_busy else "busy"}

Available rooms that can fit {persons} people:
{rooms_str}

Instructions:
- If the user's group size exceeds the room's capacity → explain clearly and suggest other rooms.
- If the room is booked → suggest an alternative room.
- If the user is busy → suggest a different time.
- If both room and time are unavailable → suggest a different room and time.
- If no suitable rooms are available → explain that directly.

Respond with:
✅ to confirm a booking
❌ if booking failed or alternatives are suggested
"""

    llm_response = call_groq_llm(prompt)

    # Simple extraction of suggestion from the LLM response
    room_match = re.search(r'Room (\d+)', llm_response)
    time_match = re.search(r'at\s+(\d{1,2}:\d{2}\s*[APMapm]{2})', llm_response)
    day_match = re.search(r'on\s+(\w+)', llm_response)

    suggested_room = f"Room {room_match.group(1)}" if room_match else None
    suggested_time = time_match.group(1) if time_match else None
    suggested_day = day_match.group(1).lower() if day_match else None

    return {
        "llm_response": llm_response,
        "room": room,
        "day": day,
        "time": time,
        "persons": persons,
        "confirmed": ("✅" in llm_response or "confirmed" in llm_response.lower()),
        "suggested_room": suggested_room,
        "suggested_time": suggested_time,
        "suggested_day": suggested_day
    }
