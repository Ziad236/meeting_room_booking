import sqlite3

DB_PATH = "booking.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                capacity INTEGER NOT NULL,
                features TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER NOT NULL,
                day TEXT NOT NULL,
                time TEXT NOT NULL,
                FOREIGN KEY(room_id) REFERENCES rooms(id)
            )
        """)
        conn.commit()

        # Sample data insertion
        rooms = [
            ("Room 1", 4, "TV,Whiteboard"),
            ("Room 2", 6, "Projector"),
            ("Room 3", 10, "Conference Phone,Whiteboard")
        ]
        conn.executemany("INSERT OR IGNORE INTO rooms (name, capacity, features) VALUES (?, ?, ?)", rooms)
        conn.commit()

def get_room_by_name(name):
    with connect_db() as conn:
        row = conn.execute("SELECT * FROM rooms WHERE name = ?", (name,)).fetchone()
        return row

def get_available_rooms(min_capacity=1):
    with connect_db() as conn:
        rows = conn.execute("SELECT * FROM rooms WHERE capacity >= ?", (min_capacity,)).fetchall()
        return [{"name": r[1], "capacity": r[2], "features": r[3]} for r in rows]

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
        return False