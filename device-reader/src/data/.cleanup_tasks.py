import sqlite3
from pathlib import Path

DB_PATH = Path("tasks.db")

def cleanup_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE status IN ('done', 'failed');
        """
    )

    conn.commit()
    conn.close()

    print("Old completed/failed tasks cleaned up.")

if __name__ == "__main__":
    cleanup_db()