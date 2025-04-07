import os

from dotenv import load_dotenv

from shared.api_client import APIClient
from shared.config import LOG_PATHS
from shared.error_handler import ErrorHandler

# 初期化（環境変数からAPIClientを構築）
load_dotenv()
client = APIClient(
    access_key   = os.getenv("ACCESS_KEY"),
    secret_key   = os.getenv("SECRET_KEY"),
    resource_id  = os.getenv("RESOURCE_ID"),
    service_name = os.getenv("SERVICE_NAME"),
    region_name  = os.getenv("REGION_NAME"),
    x_api_key    = os.getenv("X_API_KEY")
)

logger = ErrorHandler(log_file=str(LOG_PATHS["aws_client"]))

def _get_attendance():
    """AWS APIで勤怠情報を取得"""
    try:
        res = client.send_request("v1/attendance", "GET")
        return res.json()

    except Exception as e:
        logger.log_error(f"Attendance get error: {e}")
        raise