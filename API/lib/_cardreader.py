import nfc
import json
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import time
from typing import Optional

# 定数の定義
CONFIG_PATH = './config/config.json'
UID_TIMEOUT_SECONDS = 3
DEFAULT_TIMEOUT_SECONDS = 30

class ConfigError(Exception):
    """設定ファイルやキーに関するエラーを処理する例外クラス"""
    pass

class EncryptionError(Exception):
    """暗号化に関するエラーを処理する例外クラス"""
    pass

class NFCError(Exception):
    """NFCリーダーに関するエラーを処理する例外クラス"""
    pass

class ConfigLoader:
    """設定ファイルの読み込みとキーの取得を行うクラス"""

    @staticmethod
    def load_config(path: str = CONFIG_PATH) -> dict:
        if not os.path.exists(path):
            raise ConfigError(f'Config file not found: {path}')
        
        with open(path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if 'ENCRYPT_KEY' not in config['CARD_READER'] or 'ENCRYPT_IV' not in config['CARD_READER']:
            raise ConfigError("Missing 'ENCRYPT_KEY' or 'ENCRYPT_IV' in config file.")
        
        return config

class UIDEncryptor:
    """UIDを暗号化するクラス"""

    def __init__(self, key: str, iv: str):
        self.key = b64decode(key)
        self.iv = b64decode(iv)

    def encrypt_uid(self, uid: str) -> Optional[str]:
        try:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            padded_uid = pad(uid.encode('utf-8'), AES.block_size)
            encrypted_uid = cipher.encrypt(padded_uid)
            return b64encode(encrypted_uid).decode('utf-8')
        except Exception as e:
            raise EncryptionError(f"Error encrypting UID: {e}")

    def decrypt_uid(self, encrypted_uid: str) -> Optional[str]:
        try:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            decrypted_data = cipher.decrypt(b64decode(encrypted_uid))
            return unpad(decrypted_data, AES.block_size).decode('utf-8')
        except Exception as e:
            raise EncryptionError(f"Error decrypting UID: {e}")

class NFCReader:
    """NFCカードリーダーからUIDを取得するクラス"""

    @staticmethod
    def read_uid(timeout: int = DEFAULT_TIMEOUT_SECONDS) -> Optional[str]:
        clf = nfc.ContactlessFrontend('usb')
        try:
            start_time = time.time()
            tag = clf.connect(rdwr={'targets':['212F'], 'on-connect': lambda tag: False},
                              terminate=lambda: time.time() - start_time > timeout)
            return tag.identifier.hex()
        except Exception as e:
            raise NFCError(f"Error reading UID or timeout occurred: {e}")
        finally:
            clf.close()


class CardReader:
    """NFCカードからUIDを読み取り、暗号化して返すメインクラス"""

    def __init__(self):
        try:
            config = ConfigLoader.load_config()
            self.encryptor = UIDEncryptor(config['CARD_READER']['ENCRYPT_KEY'], config['CARD_READER']['ENCRYPT_IV'])
        except ConfigError as e:
            print(f'Error during initialization: {e}')
            exit(1)

    def read_and_encrypt_uid(self) -> Optional[str]:
        try:
            uid = NFCReader.read_uid(timeout=UID_TIMEOUT_SECONDS)
            if uid:
                return self.encryptor.encrypt_uid(uid)
            else:
                return None
        except (NFCError, EncryptionError) as e:
            print(f"Error: {e}")
            return None