import hashlib
import base64

class Codec:
    @staticmethod
    def _hash(text:str) -> str:
        """文字列をSHA256でハッシュ化する"""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    @staticmethod
    def base64_encode(text:str) -> str:
        """文字列をBase64エンコードする"""
        return base64.b64encode(text.encode("utf-8")).decode("utf-8")

    @staticmethod
    def base64_decode(text:str) -> str:
        """Base64エンコードされた文字列をデコードする"""
        return base64.b64decode(text.encode("utf-8")).decode("utf-8")
