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


cr = CardReader()
while True:
    #最初に表示
    print("Please Touch")
    #タッチ待ち
    cr.read()
    #リリース時の処理
    print("【 Released 】")