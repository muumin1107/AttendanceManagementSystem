import os
from dotenv import load_dotenv
from lib import APIClient, Codec, ErrorHandler

if __name__ == "__main__":
    try:
        nfc_id = "test"
        name   = "test"

        # 環境変数の読み込み
        load_dotenv()

        # APIクライアントの初期化
        api_client = APIClient(
            access_key   = os.getenv("ACCESS_KEY"),
            secret_key   = os.getenv("SECRET_KEY"),
            resource_id  = os.getenv("RESOURCE_ID"),
            service_name = os.getenv("SERVICE_NAME"),
            region_name  = os.getenv("REGION_NAME"),
            x_api_key    = os.getenv("X_API_KEY")
        )

        # APIリクエストの送信
        response = api_client.send_request(
            stage_name = "minelab-attendance-api/user",
            method     = "POST",
            data       = {
                "id"  : Codec.base64_encode(Codec._hash(nfc_id)),
                "name": Codec.base64_encode(name)
            }
        )

        # レスポンスを解析
        if not response.json().get("statusCode") == 200:
            # ステータスコードが200でない場合はエラーとみなす
            Exception(f"Failed to register user: {response.json().get('message')}")

    except Exception as e:
        ErrorHandler(log_file="/home/pi/attendance_system/API/logs/register_user.log").handle_error(e)