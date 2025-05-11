from services.room_service import connect_db

def clear_all_bookings():
    with connect_db() as conn:
        conn.execute("DELETE FROM bookings")
        conn.commit()
        print("✅ All bookings cleared.")

if __name__ == "__main__":
    clear_all_bookings()
