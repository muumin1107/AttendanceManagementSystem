#!/bin/bash

# システムのパッケージリストを更新
sudo apt update

# 必要なパッケージをインストール
cd ./src
pip install -r requirements.txt

