from fastapi import APIRouter
from app.schemas.user import UserRequest
from shared.task_queue import enqueue_task
from shared.error_handler import ErrorHandler
from shared.config import LOG_PATHS

router = APIRouter()
logger = ErrorHandler(log_file=str(LOG_PATHS["register_user"]))

@router.post("/")
async def register_user(request: UserRequest):
    try:
        enqueue_task(
            job_type = "register_user",
            params   = {
                "nfc_id": request.nfc_id,
                "name"  : request.name
            }
        )
        return {"status": "accepted", "message": "Task enqueued"}

    except Exception as e:
        logger.log_error(f"User task enqueue failed: {e}")
        return {"status": "error", "message": "Failed to enqueue user registration task"}