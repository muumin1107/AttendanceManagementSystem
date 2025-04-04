import nfc
from lib import Codec

class NFCReader:
    """NFCリーダークラス（UID読み取り & ハッシュ化）"""
    def __init__(self):
        """コンストラクタ"""
        self.hashed_id = None

    def read(self) -> str:
        """NFCタグを読み取り，UIDをハッシュ化して保持する．"""
        try:
            # NFCリーダーの初期化
            clf = nfc.ContactlessFrontend('usb')
            # NFCタグがタッチされたときのコールバック関数
            def on_connect(tag):
                uid            = tag.identifier.hex()
                self.hashed_id = Codec._hash(uid)
                return False
            # NFCタグを待機
            clf.connect(rdwr={'targets': ['212F'], 'on-connect': on_connect})
            clf.close()
            return self.hashed_id

        except OSError as e:
            raise RuntimeError(e)
        except Exception as e:
            raise RuntimeError(e)

    def clear(self):
        """保持しているハッシュIDを削除する"""
        self.hashed_id = None

# テスト用
if __name__ == "__main__":
    reader = NFCReader()
    # NFCタグを読み取る
    print("NFCタグをタッチしてください...")
    hashed_id = reader.read()
    if hashed_id:
        print(f"Hashed ID: {hashed_id}")
    else:
        print("NFCタグが読み取れませんでした．")
    # ハッシュIDをクリア
    reader.clear()