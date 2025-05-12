import sqlite3
from typing import List, Optional, Dict, Any

DB_PATH = "booking.db"


def connect_db():
    """
    Establish a connection to the SQLite database.

    Returns:
        sqlite3.Connection: Connection object.
    """
    return sqlite3.connect(DB_PATH)


def get_room_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Fetch details of a room by its name.

    Args:
        name (str): Room name (e.g., "Room 1")

    Returns:
        dict or None: Room info with id, name, capacity, and features, or None if not found.
    """
    with connect_db() as conn:
        row = conn.execute("SELECT * FROM rooms WHERE name = ?", (name,)).fetchone()
        if row:
            return {"id": row[0], "name": row[1], "capacity": row[2], "features": row[3]}
        return None


def get_available_rooms(min_capacity: int = 1) -> List[Dict[str, Any]]:
    """
    Retrieve rooms that meet or exceed a minimum capacity.

    Args:
        min_capacity (int): Minimum number of people the room must fit.

    Returns:
        List[dict]: List of room dictionaries with id, name, capacity, and features.
    """
    with connect_db() as conn:
        rows = conn.execute("SELECT * FROM rooms WHERE capacity >= ?", (min_capacity,)).fetchall()
        return [
            {"id": r[0], "name": r[1], "capacity": r[2], "features": r[3]}
            for r in rows
        ]


def has_conflict(room_name: str, day: str, time: str) -> bool:
    """
    Check whether the given room is already booked at the specified day and time.

    Args:
        room_name (str): Name of the room.
        day (str): Day of the week (e.g., "monday").
        time (str): Time in 12-hour format with AM/PM.

    Returns:
        bool: True if there is a conflict (i.e., already booked), else False.
    """
    with connect_db() as conn:
        query = """
        SELECT b.id
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
        WHERE r.name = ? AND b.day = ? AND b.time = ?
        """
        result = conn.execute(query, (room_name, day, time)).fetchone()
        return result is not None


def add_booking(room_name: str, day: str, time: str) -> bool:
    """
    Add a new booking for the given room, day, and time.

    Args:
        room_name (str): Name of the room.
        day (str): Day of the week.
        time (str): Time in 12-hour format with AM/PM.

    Returns:
        bool: True if booking was successful, False otherwise.
    """
    with connect_db() as conn:
        room = conn.execute("SELECT id FROM rooms WHERE name = ?", (room_name,)).fetchone()
        if room:
            conn.execute("INSERT INTO bookings (room_id, day, time) VALUES (?, ?, ?)", (room[0], day, time))
            conn.commit()
            return True
        print("❌ Room not found in DB:", room_name)
        return False


def get_all_bookings() -> List[Dict[str, str]]:
    """
    Retrieve all bookings along with associated room names.

    Returns:
        List[dict]: A list of dictionaries containing 'Room', 'Day', and 'Time' for each booking.
    """
    with connect_db() as conn:
        query = """
        SELECT r.name, b.day, b.time
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
        ORDER BY b.day, b.time
        """
        rows = conn.execute(query).fetchall()
        return [{"Room": row[0], "Day": row[1], "Time": row[2]} for row in rows]
