import nfc

class CardReader(object):
    def on_connect(self, tag):
        #タッチ時の処理
        print("【 Touched 】")
        return True

    def read(self):
        clf = nfc.ContactlessFrontend('usb')
        try:
            clf.connect(rdwr={'on-connect': self.on_connect})
        finally:
            clf.close()
