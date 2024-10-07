import base64
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

class CardReaderTools:
    """カードリーダーのユーティリティクラス"""
    
    def __init__(self):
        # 環境変数から暗号化キーと初期ベクトル(IV)を取得
        self.ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY').encode('utf-8')
        self.IV             = os.environ.get('IV').encode('utf-8')

        # 初期ベクトルや暗号キーの長さをチェック
        if len(self.ENCRYPTION_KEY) not in {16, 24, 32}:
            raise ValueError("Invalid ENCRYPTION_KEY length. Must be 16, 24, or 32 bytes.")
        if len(self.IV) != 16:
            raise ValueError("Invalid IV length. Must be 16 bytes.")

        # AES暗号の初期化
        self.cipher = Cipher(algorithms.AES(self.ENCRYPTION_KEY), modes.CBC(self.IV))

    def encrypt_uid(self, uid: str) -> str:
        """UIDをAESで暗号化し、base64エンコードして返す"""
        try:
            # UIDにパディングを追加（AESブロックサイズに合わせる）
            padder = padding.PKCS7(algorithms.AES.block_size).padder()
            padded_data = padder.update(uid.encode('utf-8')) + padder.finalize()

            # 暗号化処理
            encryptor = self.cipher.encryptor()
            encrypted_uid = encryptor.update(padded_data) + encryptor.finalize()

            # base64でエンコードして返す
            return base64.b64encode(encrypted_uid).decode('utf-8')
        
        except Exception as e:
            raise ValueError(f"Error during encryption: {e}")

    def decrypt_uid(self, encrypted_uid: str) -> str:
        """base64デコードされた暗号化UIDをAESで復号して返す"""
        try:
            # base64デコード
            encrypted_data = base64.b64decode(encrypted_uid)

            # 復号処理
            decryptor = self.cipher.decryptor()
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

            # パディングを削除
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

            return unpadded_data.decode('utf-8')
        
        except Exception as e:
            raise ValueError(f"Error during decryption: {e}")