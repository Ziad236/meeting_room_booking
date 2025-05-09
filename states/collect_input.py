def run(state):
    import re

    text = state.get("request", "")
    pattern = r"room (\d+).*?at (\d{1,2}:\d{2} (?:AM|PM)) on (\w+).*?(\d+) persons"
    match = re.search(pattern, text, re.IGNORECASE)

    if not match:
        return {"error": "Could not parse input. Use format: 'reserve room 2 at 3:00 PM on Monday for 6 persons'"}

    room_number = match.group(1)
    time = match.group(2)
    day = match.group(3)
    persons = match.group(4)

    return {
        "room": f"Room {room_number}",
        "time": time,
        "day": day,
        "persons": int(persons),
        "parsed": True
    }