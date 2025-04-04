import sqlite3

DB_PATH = "attendance_system.db"

if __name__ == "__main__":
    # データベースに接続（存在しない場合は作成）
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # テーブル作成（存在しない場合のみ）
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            params TEXT NOT NULL
        )
        '''
    )

    # 保存して終了
    conn.commit()
    conn.close()

    print(f"Database '{DB_PATH}' created and table 'tasks' initialized.")