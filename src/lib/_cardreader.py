import nfc
import base64
import json

from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class CardReader:
    # 設定ファイルの読み込み
    current_dir = Path(__file__).resolve().parent
    conf_path   = current_dir / '../config/config.json'
    config      = json.load(open(conf_path, 'r', encoding='utf-8'))
    # クラス変数
    ENCRYPTION_KEY = base64.b64decode(config['card']['ENCRYPTION_KEY'])
    IV  = base64.b64decode(config['card']['IV'])

    def __init__(self):
        self.clf = nfc.ContactlessFrontend('usb')
        self.uid = None

    def read_card(self):
        try:
            self.clf.connect(rdwr={'on-connect': self._on_connect})
            if self.uid:
                encrypted_uid = self._encrypt_uid(self.uid)
                return {'code': 200, 'body': encrypted_uid}
            else:
                return {'code': 400, 'body': 'Bad Request'}
        except Exception as e:
            return {'code': 500, 'body': str(e)}
        finally:
            self.clf.close()

    def _on_connect(self, tag):
        # カードのID（UID）を取得
        self.uid = tag.identifier.hex()
        return True

    def _encrypt_uid(self, uid:str) -> str:
        # AES暗号化
        backend = default_backend()
        cipher = Cipher(algorithms.AES(self.ENCRYPTION_KEY), modes.CBC(self.IV), backend=backend)
        decryptor = cipher.encryptor()
        decrypted_uid = decryptor.update(uid.encode('utf-8')) + decryptor.finalize()
        return base64.b64encode(decrypted_uid).decode('utf-8')

    def _decrypt_uid(self, encrypted_uid:str) -> str:
        # AES復号
        backend = default_backend()
        cipher = Cipher(algorithms.AES(self.ENCRYPTION_KEY), modes.CBC(self.IV), backend=backend)
        decryptor = cipher.decryptor()
        decrypted_uid = decryptor.update(base64.b64decode(encrypted_uid)) + decryptor.finalize()
        return decrypted_uid.decode('utf-8')