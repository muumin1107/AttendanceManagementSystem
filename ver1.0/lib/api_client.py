import requests
import json
from botocore.awsrequest import AWSRequest
from botocore.auth import SigV4Auth
from botocore.credentials import Credentials

class APIClient:
    """APIクライアントクラス"""
    def __init__(self, access_key:str, secret_key:str, resource_id:str, service_name:str, region_name:str, x_api_key:str) -> None:
        """コンストラクタ"""
        self.credentials  = Credentials(access_key=access_key, secret_key=secret_key)
        self.resource_id  = resource_id
        self.service_name = service_name
        self.region_name  = region_name
        self.host         = f"{resource_id}.{service_name}.{region_name}.amazonaws.com"
        self.x_api_key    = x_api_key

    def _create_signed_request(self, method:str, url:str, data:str=None) -> AWSRequest:
        """署名付きリクエストを作成する"""
        request = AWSRequest(method=method, url=url, data=data)
        # SigV4Authを使用してリクエストに署名を追加
        SigV4Auth(
            credentials  = self.credentials,
            service_name = self.service_name,
            region_name  = self.region_name
        ).add_auth(request=request)
        return request

    def _get_headers(self, request:AWSRequest) -> dict:
        """リクエストヘッダーを取得する"""
        return {
            "Authorization": request.headers["Authorization"],
            "Host"         : self.host,
            "X-Amz-Date"   : request.headers["X-Amz-Date"],
            "X-Api-Key"    : self.x_api_key,
            "Content-Type" : "application/json"
        }

    def send_request(self, stage_name:str, method:str, params:dict=None, data:dict=None, timeout:int=10):
        """リクエストを送信する"""
        # リクエストのURLを作成
        url     = f"https://{self.host}/{stage_name}"
        request = self._create_signed_request(method=method, url=url, data=json.dumps(data))
        headers = self._get_headers(request=request)
        # リクエストを送信
        if method == "GET":
            response = requests.request(
                url     = url,
                method  = method,
                headers = headers,
                params  = params,
                data    = json.dumps(data),
                timeout = timeout
            )
        elif method == "POST":
            response = requests.request(
                url     = url,
                method  = method,
                headers = headers,
                data    = json.dumps(data),
                timeout = timeout
            )
        else:
            raise ValueError(f"Unsupported method: {method}. Supported methods are GET and POST.")
        # HTTPエラーが発生した場合は例外をスロー
        response.raise_for_status()
        return response
