import sqlite3

DB_PATH = "booking.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

def get_room_by_name(name):
    with connect_db() as conn:
        row = conn.execute("SELECT * FROM rooms WHERE name = ?", (name,)).fetchone()
        if row:
            return {"id": row[0], "name": row[1], "capacity": row[2], "features": row[3]}
        return None

def get_available_rooms(min_capacity=1):
    with connect_db() as conn:
        rows = conn.execute("SELECT * FROM rooms WHERE capacity >= ?", (min_capacity,)).fetchall()
        return [
            {"id": r[0], "name": r[1], "capacity": r[2], "features": r[3]}
            for r in rows
        ]

def has_conflict(room_name, day, time):
    with connect_db() as conn:
        query = """
        SELECT b.id
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
        WHERE r.name = ? AND b.day = ? AND b.time = ?
        """
        result = conn.execute(query, (room_name, day, time)).fetchone()
        return result is not None

def add_booking(room_name, day, time):
    with connect_db() as conn:
        room = conn.execute("SELECT id FROM rooms WHERE name = ?", (room_name,)).fetchone()
        if room:
            conn.execute("INSERT INTO bookings (room_id, day, time) VALUES (?, ?, ?)", (room[0], day, time))
            conn.commit()
            return True
        print("❌ Room not found in DB:", room_name)
        return False


def get_all_bookings():
    with connect_db() as conn:
        query = """
        SELECT r.name, b.day, b.time
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
        ORDER BY b.day, b.time
        """
        rows = conn.execute(query).fetchall()
        return [{"Room": row[0], "Day": row[1], "Time": row[2]} for row in rows]
