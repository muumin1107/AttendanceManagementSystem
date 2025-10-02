import boto3

class CognitoClient:
    """Cognitoクライアントクラス"""
    def __init__(self, identity_pool_id: str, region_name: str) -> None:
        """コンストラクタ"""
        self.identity_pool_id = identity_pool_id
        self.region_name      = region_name

    def get_cognito_credentials(self) -> dict:
        """Cognitoから一時的なAWS認証情報を取得する"""
        cognito_client = boto3.client("cognito-identity", region_name=self.region_name)

        # CognitoからIDを取得
        response_id = cognito_client.get_id(IdentityPoolId=self.identity_pool_id)
        identity_id = response_id['IdentityId']

        # 取得したIDを使って一時的なAWS認証情報を取得
        response_creds = cognito_client.get_credentials_for_identity(IdentityId=identity_id)
        credentials    = response_creds['Credentials']

        return {
            "access_key"   : credentials['AccessKeyId'],
            "secret_key"   : credentials['SecretKey'],
            "session_token": credentials['SessionToken']
        }