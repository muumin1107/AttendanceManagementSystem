# 【ラズパイ】カードリーダー式勤怠管理システム

RaspberryPiを使ったカードリーダー式の勤怠管理システムを作成します．

## システム概要図

![システム概要図](https://github.com/user-attachments/assets/a20b3635-1b43-4e50-9d1c-3dc4e589fe4a)

## ユーザーインターフェース（一部）

![UIイメージ](https://github.com/user-attachments/assets/dcf3c998-1461-49b9-8bcf-6be652ccdd0f)

## RaspberryPiのセットアップ

- RaspberryPi 4 Model B

| Raspberry Pi Imager | OS | Kernel |
----|----|----
| v1.8.5 | Raspbian 11.9 | 6.1.21 |

```
$ sudo apt update
$ cd ~/
$ mkdir .ssh
$ touch .ssh/authorized_keys
$ nano .ssh/authorized_keys

// 自身の公開鍵（.pub）をコピペ

$ sudo reboot
```

## カードリーダー接続

Raspberry Pi 4 Model BにRC-S380/Sを接続する．
- RC-S380/S

```
$ lsusb

// Sony Corp. RC-S380/Sが認識されていることを確認

$ sudo pip install nfcpy

// nfcが適切にインストールされているかを確認
$ git clone https://github.com/nfcpy/nfcpy.git
$ sudo python3 nfcpy/examples/tagtool.py show

// NFCカードを近づけて情報が表示されればOK

$ python3 -m nfc

// better assign ... と記載されている下の行に提示されたコマンドを入力
$ sudo sh -c 'echo SUBSYSTEM==\"usb\", ACTION==\"add\", ATTRS{idVendor}==\"054c\", ATTRS{idProduct}==\"06c1\", GROUP=\"plugdev\" >> /etc/udev/rules.d/nfcdev.rules'
$ sudo udevadm control -R # then re-attach device
```

## API仕様
| API Name | Argument | note |
----|----|----
| register_id | tid_num, name, attribute, discription | ID情報の登録用API |
| register_attendance | id_num, next_state | 勤怠情報の登録用API |
| remove_data | id_num, mode, name | ID/勤怠DB情報の削除用API |
| health | - | ヘルスチェック用のAPI |
