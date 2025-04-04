import nfc

class NFCReader:
    """NFCリーダークラス"""
    def __init__(self):
        """コンストラクタ"""
        self.clf = nfc.ContactlessFrontend('usb')
        self.tag = None

    def close(self):
        """クローズ"""
        if self.clf:
            self.clf.close()
        self.clf = None
        self.tag = None

# テスト用
if __name__ == "__main__":
    try:
        reader = NFCReader()
        print("NFC Reader initialized successfully.")

    except Exception as e:
        print(f"Error initializing NFC Reader: {e}")
    finally:
        reader.close()