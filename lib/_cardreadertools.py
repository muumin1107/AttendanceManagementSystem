import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

class CardReaderTools:
    """カードリーダーのユーティリティクラス"""

    # 定数定義
    AES_BLOCK_SIZE = algorithms.AES.block_size
    VALID_KEY_LENGTHS = {16, 24, 32}
    IV_LENGTH = 16

    def __init__(self):
        """暗号化キーと初期ベクトル(IV)を環境変数から取得し、初期化"""
        encryption_key = os.environ.get('ENCRYPTION_KEY')
        iv = os.environ.get('IV')

        if not encryption_key or not iv:
            raise ValueError("ENCRYPTION_KEY and IV must be set in the environment variables.")

        self.ENCRYPTION_KEY = encryption_key.encode('utf-8')
        self.IV = iv.encode('utf-8')

        # 暗号キーと初期ベクトルの長さをチェック
        self._validate_key_and_iv()

    def _validate_key_and_iv(self):
        """暗号キーと初期ベクトルの長さを検証"""
        if len(self.ENCRYPTION_KEY) not in self.VALID_KEY_LENGTHS:
            raise ValueError(f"Invalid ENCRYPTION_KEY length. Must be 16, 24, or 32 bytes.")
        if len(self.IV) != self.IV_LENGTH:
            raise ValueError(f"Invalid IV length. Must be {self.IV_LENGTH} bytes.")

    def _get_cipher(self) -> Cipher:
        """AES暗号化のCipherオブジェクトを生成"""
        return Cipher(algorithms.AES(self.ENCRYPTION_KEY), modes.CBC(self.IV))

    def encrypt_uid(self, uid: str) -> str:
        """UIDをAESで暗号化し、base64エンコードして返す"""
        try:
            # UIDにパディングを追加（AESのブロックサイズに合わせる）
            padder = padding.PKCS7(self.AES_BLOCK_SIZE).padder()
            padded_data = padder.update(uid.encode('utf-8')) + padder.finalize()

            # 暗号化処理
            cipher = self._get_cipher()
            encryptor = cipher.encryptor()
            encrypted_uid = encryptor.update(padded_data) + encryptor.finalize()

            # base64でエンコードして返す
            return base64.b64encode(encrypted_uid).decode('utf-8')

        except Exception as e:
            raise ValueError(f"Error during encryption: {e}")

    def decrypt_uid(self, encrypted_uid: str) -> str:
        """base64でエンコードされた暗号化UIDをAESで復号して返す"""
        try:
            # base64デコード
            encrypted_data = base64.b64decode(encrypted_uid)

            # 復号処理
            cipher = self._get_cipher()
            decryptor = cipher.decryptor()
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

            # パディングを削除
            unpadder = padding.PKCS7(self.AES_BLOCK_SIZE).unpadder()
            unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

            return unpadded_data.decode('utf-8')

        except Exception as e:
            raise ValueError(f"Error during decryption: {e}")