from pydantic import BaseModel

class UserRequest(BaseModel):
    nfc_id: str
    name  : str