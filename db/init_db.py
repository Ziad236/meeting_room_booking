from services.db import init_db

if __name__ == "__main__":
    """
    Initializes the database schema and inserts sample room data.
    This script should be run once before using the application.
    """
    init_db()
    print("✅ Database initialized and sample rooms inserted.")
