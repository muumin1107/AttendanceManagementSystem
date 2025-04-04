import os
from dotenv import load_dotenv
from shared.api_client import APIClient
from shared.codec import Codec
from shared.error_handler import ErrorHandler
from shared.config import LOG_PATHS

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

logger = ErrorHandler(log_file=LOG_PATHS["aws_client"])

def register_user(nfc_id: str, name: str):
    """AWS APIでユーザー登録"""
    data = {
        "nfc_id": nfc_id,
        "name"  : name
    }
    try:
        res = client.send_request("v1/user", "POST", data=data)
        return res.json()

    except Exception as e:
        logger.log_error(f"User registration failed: {e}")
        raise

def register_attendance(nfc_id: str, status: str):
    """AWS APIで勤怠登録"""
    data = {
        "nfc_id": nfc_id,
        "status": status
    }
    try:
        res = client.send_request("v1/attendance", "POST", data=data)
        return res.json()

    except Exception as e:
        logger.log_error(f"Attendance registration failed: {e}")
        raise

def get_user(nfc_id: str):
    """AWS APIでユーザー情報（ユーザー名）取得"""
    try:
        res = client.send_request(
            stage_name = "v1/user",
            method     = "GET",
            params     = {"id": Codec.base64_encode(nfc_id)}
        )
        return res.json()

    except Exception as e:
        logger.log_error(f"User lookup failed: {e}")
        raise