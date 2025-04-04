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

# テスト用
if __name__ == "__main__":
    # ハッシュ化のテスト
    text = "Hello, World!"
    hashed_text = Codec._hash(text)
    print(f"Original: {text}")
    print(f"Hashed: {hashed_text}")

    # Base64エンコードのテスト
    encoded_text = Codec.base64_encode(text)
    print(f"Encoded: {encoded_text}")

    # Base64デコードのテスト
    decoded_text = Codec.base64_decode(encoded_text)
    print(f"Decoded: {decoded_text}")