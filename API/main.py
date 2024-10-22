from lib._cardreader import CardReader, NFCError, EncryptionError
from lib._attendancesystemoperation import AttendanceSystemOperation

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict

# FastAPIのインスタンスを生成
app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# リクエストボディのスキーマを定義
class Response(BaseModel):
    code: int
    message: str

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
def read_root() -> Dict[str, str]:
    """
    APIのルートエンドポイント。ウェルカムメッセージを返す。
    """
    return {"message": "Hello API Server!"}

# ヘルスチェックエンドポイント
@app.get("/health")
def health_check() -> Dict[str, str]:
    """
    サービスの稼働状況を確認するエンドポイント。
    """
    return {"message": "Service is up and running"}

# ID取得エンドポイント
@app.get("/get_uid")
def get_uid() -> JSONResponse:
    """
    カードリーダーからUIDを取得し、暗号化するエンドポイント。

    Returns:
        JSONResponse: 暗号化されたUIDを含むレスポンス、またはエラーレスポンス
    """
    try:
        # CardReaderのインスタンスを生成
        cardreader = CardReader()
        # UIDを読み取り、暗号化した結果を取得
        encrypted_uid = cardreader.read_and_encrypt_uid()

        # UIDが取得できなかった場合
        if encrypted_uid is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, 
                content={"message": "Failed to read and encrypt UID"}
            )

        # 正常に取得・暗号化できた場合
        return JSONResponse(
            status_code=status.HTTP_200_OK, 
            content={"uid": encrypted_uid}
        )

    except NFCError as e:
        # NFC関連のエラー
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content={"message": f"NFC Error: {str(e)}"}
        )
    except EncryptionError as e:
        # 暗号化関連のエラー
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content={"message": f"Encryption Error: {str(e)}"}
        )
    except Exception as e:
        # その他の予期しないエラー
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content={"message": f"Unexpected error: {str(e)}"}
        )

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