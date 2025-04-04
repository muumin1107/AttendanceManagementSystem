import os
from dotenv import load_dotenv
from lib import APIClient, ErrorHandler

if __name__ == "__main__":
    try:
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
            stage_name = "v1/attendance",
            method     = "GET"
        )

        # レスポンスを解析
        if response.status_code != 200:
            ErrorHandler(log_file="/home/pi/attendance_system/API/logs/get_attendance.log").log_error(f"Error: {response.json()}")
        # レスポンスを表示
        print(response.json())

    except Exception as e:
        ErrorHandler(log_file="/home/pi/attendance_system/API/logs/get_attendance.log").handle_error(e)