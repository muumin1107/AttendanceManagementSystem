from lib._api import AttendanceSystemOperation
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

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
def register_id(id: str, name: str, attribute: str, description: str) -> dict:
    """
    IDを登録するエンドポイント。

    Args:
        id (str): ユーザーのID。
        name (str): ユーザーの名前。
        attribute (str): 属性（例: ICカード, スマートフォン）。
        description (str): 備考。

    Returns:
        dict: 登録結果メッセージ。
    """
    try:
        result = AttendanceSystemOperation.register_id(id=id, name=name, attribute=attribute, description=description)
        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(result))
        return {"code": status.HTTP_200_OK, "message": "ID registration successful"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# ID削除エンドポイント
@app.delete("/remove_id")
def remove_id(id: str, name: str) -> dict:
    """
    IDを削除するエンドポイント。

    Args:
        id (str): ユーザーのID。
        name (str): ユーザーの名前。

    Returns:
        dict: 削除結果メッセージ。
    """
    try:
        result = AttendanceSystemOperation.remove_id(id=id, name=name)
        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(result))
        return {"code": status.HTTP_200_OK, "message": "ID removal successful"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# 勤怠登録エンドポイント
@app.post("/register_attendance")
def register_attendance(id: str, next_state: str) -> dict:
    """
    勤怠状態を登録するエンドポイント。

    Args:
        id (str): ユーザーのID。
        next_state (str): 次の状態（例: 出勤, 退勤）。

    Returns:
        dict: 登録結果メッセージ。
    """
    try:
        result = AttendanceSystemOperation.register_attendance(id=id, next_state=next_state)
        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(result))
        return {"code": status.HTTP_200_OK, "message": "Attendance registration successful"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# 勤怠削除エンドポイント
@app.delete("/remove_attendance")
def remove_attendance(id: str, name: str) -> dict:
    """
    勤怠データを削除するエンドポイント。

    Args:
        id (str): ユーザーのID。
        name (str): ユーザーの名前。

    Returns:
        dict: 削除結果メッセージ。
    """
    try:
        result = AttendanceSystemOperation.remove_attendance(id=id, name=name)
        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(result))
        return {"code": status.HTTP_200_OK, "message": "Attendance removal successful"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))