import json

from fastapi import APIRouter

from shared.aws_client import _get_attendance
from shared.config import LOG_PATHS
from shared.error_handler import ErrorHandler

router = APIRouter()
logger = ErrorHandler(log_file=str(LOG_PATHS["get_attendance"]))

@router.get("/")
def get_attendance():
    try:
        res = _get_attendance()
        return {"statusCode": 200, "data": res}

    except Exception as e:
        logger.log_error(f"Attendance : {e}")
        return {"statusCode": 500, "message": "Failed to get attendance data"}