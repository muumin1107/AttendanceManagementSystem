import base64
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class CardReaderTools:
    def __init__(self):
        # 環境変数の取得
        self.ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY').encode('utf-8')
        self.IV             = os.environ.get('IV').encode('utf-8')
        # ID情報の初期化
        self.uid            = None

    def encrypt_uid(self, uid:str) -> str:
        # AES暗号化
        backend = default_backend()
        cipher = Cipher(algorithms.AES(self.ENCRYPTION_KEY), modes.CBC(self.IV), backend=backend)
        decryptor = cipher.encryptor()
        decrypted_uid = decryptor.update(uid.encode('utf-8')) + decryptor.finalize()
        return base64.b64encode(decrypted_uid).decode('utf-8')

    def decrypt_uid(self, encrypted_uid:str) -> str:
        # AES復号
        backend = default_backend()
        cipher = Cipher(algorithms.AES(self.ENCRYPTION_KEY), modes.CBC(self.IV), backend=backend)
        decryptor = cipher.decryptor()
        decrypted_uid = decryptor.update(base64.b64decode(encrypted_uid)) + decryptor.finalize()
        return decrypted_uid.decode('utf-8')