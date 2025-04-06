from fastapi import FastAPI

from app.api import attendance, card, user

app = FastAPI()

app.include_router(attendance.router, prefix="/v1/attendance")
app.include_router(user.router, prefix="/v1/user")
app.include_router(card.router, prefix="/v1/card")