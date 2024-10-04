# カードリーダー式勤怠管理システム with RaspberryPi

RaspberryPiを使ったカードリーダー式の勤怠管理システムを作成します．

## システム概要図

![システム概要図](https://github.com/user-attachments/assets/a20b3635-1b43-4e50-9d1c-3dc4e589fe4a)

## ユーザーインターフェース（一部）

![UIイメージ](https://github.com/user-attachments/assets/dcf3c998-1461-49b9-8bcf-6be652ccdd0f)

## 開発環境

- RaspberryPi 4 Model B
- RC-S380/S

## RaspberryPiのセットアップ

- Raspberry Pi Imager v1.8.5
- Raspbian 11.9
- Kernel 6.1.21

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


## インストール手順

```
$ cd ~/
$ mkdir {任意のワークフォルダ}
$ cd {任意のワークフォルダ}
$ git clone https://github.com/haradakaito/AttendanceManagementSystem.git
$ pip install --upgrade pip
$ pip install requirements.txt
```
