from pydantic import BaseModel

class AttendanceRequest(BaseModel):
    nfc_id: str
    status: str