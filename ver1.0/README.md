# 【ラズパイ】カードリーダー式勤怠管理システム

RaspberryPiを使ったカードリーダー式の勤怠管理システムを作成します．

## システム概要図

![システム概要図_ver2 0](https://github.com/user-attachments/assets/c394879f-60c0-4dfd-8088-f7ca5087e160)

## ユーザーインターフェース（一部）

- **勤怠画面**

![スクリーンショット 2024-10-21 113408](https://github.com/user-attachments/assets/b42a4a17-4704-49aa-8b9f-da681d2f5fba)

![入力フォーム](https://github.com/user-attachments/assets/254fab70-aec4-468a-b115-f822b46bf780)

![カード読み込み画面](https://github.com/user-attachments/assets/efbf70c6-7fd6-48c0-8cf9-7a5c4332f5f1)

## RaspberryPiのセットアップ

- RaspberryPi 4 Model B

| Raspberry Pi Imager | OS            | Kernel |
----|----|----
| v1.8.5              | Raspbian 11.9 | 6.1.21 |

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
