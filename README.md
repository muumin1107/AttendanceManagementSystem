# 勤怠管理システム

RaspberryPiを使ったカードリーダー式の勤怠管理システムを作成します．

## システム概要図

![alt text](システム概要図.png)

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