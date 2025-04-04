from pathlib import Path

# プロジェクトルートディレクトリ
BASE_DIR = Path(__file__).resolve().parent.parent

# ログディレクトリとログファイルパス
LOG_DIR = BASE_DIR.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_PATHS = {
    "card_reader"        : LOG_DIR / "card_reader.log",
    "register_attendance": LOG_DIR / "register_attendance.log",
    "register_user"      : LOG_DIR / "register_user.log",
    "aws_client"         : LOG_DIR / "aws_client.log",
}

# データディレクトリとDBファイルパス
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "tasks.db"