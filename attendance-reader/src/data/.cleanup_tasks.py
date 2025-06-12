import sqlite3
from pathlib import Path

DB_PATH = Path("tasks.db")

def cleanup_db():
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE status IN ('done', 'failed');
        """
    )

    conn.commit()
    conn.close()

    print("Cleanup completed: Removed 'done' and 'failed' tasks from the database.")

if __name__ == "__main__":
    cleanup_db()