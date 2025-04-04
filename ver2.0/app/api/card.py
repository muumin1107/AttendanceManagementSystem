from fastapi import APIRouter
from app.services.card_service import read_card_uid

router = APIRouter()

@router.get("/read")
async def read_card():
    try:
        hashed_id = read_card_uid()
        return {"status": "success", "nfc_id": hashed_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}