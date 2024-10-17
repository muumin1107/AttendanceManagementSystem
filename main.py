from lib._api import AttendanceSystemOperation
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# FastAPIのインスタンスを生成
app = FastAPI()

# リクエストボディのスキーマを定義
class RegisterIdRequest(BaseModel):
    id: str
    name: str
    attribute: str
    description: str

class RemoveIdRequest(BaseModel):
    id: str
    name: str

class RegisterAttendanceRequest(BaseModel):
    id: str
    next_state: str

class RemoveAttendanceRequest(BaseModel):
    id: str
    name: str

# レスポンスボディのスキーマを定義
class Response(BaseModel):
    code: int
    message: str

# ルートエンドポイント
@app.get("/")
def read_root() -> dict:
    """
    APIのルートエンドポイント。ウェルカムメッセージを返す。
    """
    return {"message": "Welcome to the Attendance System API"}

# ヘルスチェックエンドポイント
@app.get("/health")
def health_check() -> dict:
    """
    サービスの稼働状況を確認するエンドポイント。
    """
    return {"message": "Service is up and running"}

# ID登録エンドポイント
@app.post("/register_id")
def register_id(request: RegisterIdRequest) -> JSONResponse:
    """
    IDを登録するエンドポイント。

    Args:
        request (RegisterIdRequest): リクエストボディ。

    Returns:
        JSONResponse: 登録結果メッセージ。
    """
    try:
        result = AttendanceSystemOperation().register_id(id=request.id, name=request.name, attribute=request.attribute, description=request.description)
        if result == True:
            return JSONResponse(content=Response(code=status.HTTP_200_OK, message="ID registration successful").dict(), status_code=status.HTTP_200_OK)
        return JSONResponse(content=Response(code=status.HTTP_400_BAD_REQUEST, message=str(result)).dict(), status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JSONResponse(content=Response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)).dict(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ID削除エンドポイント
@app.delete("/remove_id")
def remove_id(request: RemoveIdRequest) -> JSONResponse:
    """
    IDを削除するエンドポイント。

    Args:
        request (RemoveIdRequest): リクエストボディ。

    Returns:
        JSONResponse: 削除結果メッセージ。
    """
    try:
        result = AttendanceSystemOperation().remove_id(id=request.id, name=request.name)
        if result == True:
            return JSONResponse(content=Response(code=status.HTTP_200_OK, message="ID removal successful").dict(), status_code=status.HTTP_200_OK)
        return JSONResponse(content=Response(code=status.HTTP_400_BAD_REQUEST, message=str(result)).dict(), status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JSONResponse(content=Response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)).dict(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 勤怠登録エンドポイント
@app.post("/register_attendance")
def register_attendance(request: RegisterAttendanceRequest) -> JSONResponse:
    """
    勤怠状態を登録するエンドポイント。

    Args:
        request (RegisterAttendanceRequest): リクエストボディ。

    Returns:
        JSONResponse: 登録結果メッセージ。
    """
    try:
        result = AttendanceSystemOperation().register_attendance(id=request.id, next_state=request.next_state)
        if result == True:
            return JSONResponse(content=Response(code=status.HTTP_200_OK, message="Attendance registration successful").dict(), status_code=status.HTTP_200_OK)
        return JSONResponse(content=Response(code=status.HTTP_400_BAD_REQUEST, message=str(result)).dict(), status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JSONResponse(content=Response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)).dict(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 勤怠削除エンドポイント
@app.delete("/remove_attendance")
def remove_attendance(request: RemoveAttendanceRequest) -> JSONResponse:
    """
    勤怠データを削除するエンドポイント。

    Args:
        request (RemoveAttendanceRequest): リクエストボディ。

    Returns:
        JSONResponse: 削除結果メッセージ。
    """
    try:
        result = AttendanceSystemOperation().remove_attendance(id=request.id, name=request.name)
        if result == True:
            return JSONResponse(content=Response(code=status.HTTP_200_OK, message="Attendance removal successful").dict(), status_code=status.HTTP_200_OK)
        return JSONResponse(content=Response(code=status.HTTP_400_BAD_REQUEST, message=str(result)).dict(), status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JSONResponse(content=Response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)).dict(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)