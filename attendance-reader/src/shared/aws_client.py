import os
from dotenv import load_dotenv

from shared.api_client     import APIClient
from shared.cognito_client import CognitoClient
# from shared.sm_client      import SMClient
from shared.codec          import Codec
from shared.config         import LOG_PATHS
from shared.error_handler  import ErrorHandler

# 初期化
load_dotenv()

# 一時的な認証情報を取得する
cognito_client = CognitoClient(
    identity_pool_id = os.getenv("IDENTITY_POOL_ID"),
    region_name      = os.getenv("REGION_NAME")
)
cognito_creds = cognito_client.get_cognito_credentials()

# SecretManagerからAPIキーを取得する
# sm_client = SMClient(
#     region_name   = os.getenv("REGION_NAME"),
#     access_key    = cognito_creds["access_key"],
#     secret_key    = cognito_creds["secret_key"],
#     session_token = cognito_creds["session_token"],
#     secret_arn    = os.getenv("SECRET_ARN")
# )
# sm_creds = sm_client.get_api_key()


api_client = APIClient(
    access_key    = cognito_creds["access_key"],
    secret_key    = cognito_creds["secret_key"],
    session_token = cognito_creds["session_token"],
    resource_id   = os.getenv("RESOURCE_ID"),
    service_name  = os.getenv("SERVICE_NAME"),
    region_name   = os.getenv("REGION_NAME"),
    x_api_key     = os.getenv("X_API_KEY")
    # x_api_key     = sm_creds["x-api-key"]
)

logger = ErrorHandler(log_file=str(LOG_PATHS["aws_client"]))

def register_user(id: str, name: str, grade:str):
    """AWS APIでユーザー登録"""
    data = {
        "id"   : Codec.base64_encode(id),
        "name" : Codec.base64_encode(name),
        "grade": Codec.base64_encode(grade)
    }
    try:
        res = api_client.send_request("v1/user", "POST", data=data)
        return res.json()

    except Exception as e:
        logger.log_error(f"User registration failed: {e}")
        raise

def register_attendance(id: str, status: str):
    """AWS APIで勤怠登録"""
    data = {
        "id"    : Codec.base64_encode(id),
        "status": Codec.base64_encode(status)
    }
    try:
        res = api_client.send_request("v1/attendance", "POST", data=data)
        return res.json()

    except Exception as e:
        logger.log_error(f"Attendance registration failed: {e}")
        raise


# if __name__ == '__main__':
#     """
#     このスクリプトが直接実行された場合に、以下の処理を行う
#     (例: python -m shared.aws_client)
#     """
#     try:
#         print("--- Main process started ---")
        
#         # 例として、勤怠登録APIを呼び出す
#         user_id = "92ac2e7ad130b70c0b98bf31c86fb077c60401be443f36f32c18df949cc45136"
#         status = "clock_in"
        
#         print(f"Attempting to register attendance for user: {user_id}")
#         response = register_attendance(id=user_id, status=status)
        
#         print("--- API call successful ---")
#         print("Status Code:", response.get("statusCode") or "N/A")
#         print("Response Body:", response.get("body") or "N/A")

#     except Exception as e:
#         # logger を使ってエラーを記録することも可能
#         logger.log_error(f"An error occurred in the main process: {e}")
#         print(f"An error occurred in the main process: {e}")
    
#     finally:
#         print("--- Script finished ---")