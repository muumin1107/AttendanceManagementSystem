from pathlib import Path

# プロジェクトルートディレクトリ
BASE_DIR = "/home/pi/attendance_system_api"

# ログファイルのパス
LOG_PATHS = {
    "get_attendance": Path(BASE_DIR) / "logs" / "get_attendance.log",
    "aws_client"    : Path(BASE_DIR) / "logs" / "aws_client.log",
}