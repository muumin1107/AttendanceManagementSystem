import os

from dotenv import load_dotenv

from shared.api_client    import APIClient
from shared.codec         import Codec
from shared.config        import LOG_PATHS
from shared.error_handler import ErrorHandler

# 初期化
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

def register_user(id: str, name: str, grade:str):
    """AWS APIでユーザー登録"""
    data = {
        "id"   : Codec.base64_encode(id),
        "name" : Codec.base64_encode(name),
        "grade": Codec.base64_encode(grade)
    }
    try:
        res = client.send_request("v1/user", "POST", data=data)
        return res.json()

    except Exception as e:
        logger.log_error(f"User registration failed: {e}")
        raise

def register_attendance(id: str, status: str):
    """AWS APIで勤怠登録"""
    data = {
        "id"    : Codec.base64_encode(id),
        "status": Codec.base64_encode(status)
    }
    try:
        res = client.send_request("v1/attendance", "POST", data=data)
        return res.json()

    except Exception as e:
        logger.log_error(f"Attendance registration failed: {e}")
        raise