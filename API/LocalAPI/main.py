from lib._cardreader import CardReader, NFCError, EncryptionError
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