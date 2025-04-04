from fastapi import APIRouter
from app.schemas.attendance import AttendanceRequest
from shared.task_queue import enqueue_task
from shared.error_handler import ErrorHandler
from shared.config import LOG_PATHS

router = APIRouter()
logger = ErrorHandler(log_file=str(LOG_PATHS["register_attendance"]))

@router.post("/")
async def register_attendance(request: AttendanceRequest):
    try:
        enqueue_task(
            job_type = "register_attendance",
            params   = {
                "nfc_id": request.nfc_id,
                "status": request.status,
            }
        )
        return {"status": "accepted", "message": "Task enqueued"}

    except Exception as e:
        logger.log_error(f"Attendance task enqueue failed: {e}")
        return {"status": "error", "message": "Failed to enqueue attendance task"}