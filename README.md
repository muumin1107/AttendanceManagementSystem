# 【ラズパイ】カードリーダー式勤怠管理システム

RaspberryPiを使ったカードリーダー式の勤怠管理システムを作成します．

## システム概要図

![システム概要図](https://github.com/user-attachments/assets/a20b3635-1b43-4e50-9d1c-3dc4e589fe4a)

## ユーザーインターフェース（一部）

![UIイメージ](https://github.com/user-attachments/assets/dcf3c998-1461-49b9-8bcf-6be652ccdd0f)

![スクリーンショット 2024-10-05 010857](https://github.com/user-attachments/assets/5674eae6-a726-4d0d-bd5d-3a5e1e9ed21b)

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


## インストール手順

- requirements.txt

| Library | Version |
----|----
| notion-client | 2.2.1 |
| nfcpy | 1.0.4 |
| cryptrography | 43.0.1 |

```
$ cd ~/
$ mkdir {任意のワークフォルダ}
$ cd {任意のワークフォルダ}
$ git clone https://github.com/haradakaito/AttendanceManagementSystem.git
$ pip install --upgrade pip
$ pip install requirements.txt
```
