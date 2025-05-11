def run(state):
    import re

    text = state.get("request", "")
    pattern = r"room (\d+).*?at (\d{1,2}:\d{2} (?:AM|PM)) on (\w+).*?(\d+) persons"
    match = re.search(pattern, text, re.IGNORECASE)

    if not match:
        return {"error": "❌ Could not parse input. Please use this format:\n'reserve room 2 at 3:00 PM on Monday for 6 persons'"}

    room_number = match.group(1)
    time = match.group(2)
    day = match.group(3).strip().lower()
    persons = match.group(4)

    if not all([room_number, time, day, persons]):
        return {"error": "❌ Missing one or more fields. Please provide room number, time, day, and number of persons."}

    return {
        "room": f"Room {room_number}",
        "time": time,
        "day": day,
        "persons": int(persons),
        "parsed": True
    }
