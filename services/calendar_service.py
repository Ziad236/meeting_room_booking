# calendar_service.py

# Hardcoded fake conflicts for Room 2 at 3:00 PM on Monday
conflict_data = {
    "Room 2": {
        "Monday": ["3:00 PM"]
    }
}

def has_conflict(room, day, time):
    return time in conflict_data.get(room, {}).get(day, [])