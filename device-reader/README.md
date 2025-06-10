# 【Raspberry Pi】カードリーダー式在室確認システム（device-reader）

## システム環境

- Raspberry Pi 4B（device-reader）

| Raspberry Pi Imager | OS                               | Kernel     |
----                  |----                              |----
| v1.8.5              | Raspbian GNU/Linux 11 (bullseye) | 6.1.21-v8+ |

- FastAPI（ローカルAPIサーバー）
- SQLite（バッファ）
- RC-S380 S（カードリーダー）

## プロジェクト構成

```
.
├── app/                                # アプリケーション本体（FastAPI）
│   ├── __init__.py
│   ├── main.py                         # FastAPI アプリのエントリーポイント
│   ├── api/                            # API エンドポイント定義
│   │   ├── __init__.py
│   │   ├── attendance.py               # 勤怠登録 API
│   │   ├── card.py                     # NFCカード読み取り API
│   │   └── user.py                     # ユーザー登録 API
│   ├── hardware/
│   │   └── card_reader.py              # NFCカードリーダー操作
│   ├── schemas/                        # リクエスト/レスポンス用スキーマ
│   │   ├── __init__.py
│   │   ├── attendance.py
│   │   └── user.py
│   └── services/
│       └── card_service.py             # ハードウェア連携ロジック
│
├── data/                               # ローカルデータベース・初期化スクリプト
│   ├── .cleanup_tasks.py               # 古いタスクの自動削除スクリプト
│   ├── .init_db.py                     # SQLite DB初期化スクリプト
│   └── tasks.db                        # タスクキュー用データベース
│
├── logs/                               # ログファイル出力ディレクトリ
│   ├── aws_client.log
│   ├── card_reader.log
│   ├── register_attendance.log
│   ├── register_user.log
│   └── worker.log
│
├── shared/                             # 共通処理・設定・ユーティリティ
│   ├── __init__.py
│   ├── api_client.py                   # ローカル API 呼び出し用
│   ├── aws_client.py                   # AWS Lambda 呼び出し用
│   ├── codec.py                        # NFC ID エンコード/デコード
│   ├── config.py                       # 設定・環境変数読み込み
│   ├── error_handler.py                # ログ付き例外処理
│   └── task_queue.py                   # タスク登録・取得・状態管理
│
├── web/frontend                        # フロントエンド（React + TypeScript）
│   ├── .env                            # フロント用環境変数（API URL等）
│   ├── public/
│   │   └── ...                         # 静的ファイル（favicon, index.html等）
│   ├── src/
│   │   ├── api/                        # APIクライアント（fetchラッパー）
│   │   │   ├── attendance.ts
│   │   │   ├── cardReader.ts
│   │   │   └── user.ts
│   │   ├── hooks/                      # カスタムフック
│   │   │   ├── useCardReader.ts
│   │   │   ├── useCurrentTime.ts
│   │   │   ├── useRegisterAttendance.ts
│   │   │   ├── useRegisterUser.ts
│   │   │   └── useTimeOfDay.ts
│   │   ├── pages/                      # ページごとのコンポーネント
│   │   │   ├── HomePage/
│   │   │   │   ├── HomePage.tsx
│   │   │   │   └── HomePage.css
│   │   │   ├── RegisterAttendance/
│   │   │   │   ├── AttendanceCardWaitPage.tsx
│   │   │   │   └── AttendanceCardWaitPage.css
│   │   │   └── RegisterUser/
│   │   │       ├── UserCardWaitPage.tsx
│   │   │       ├── UserCardWaitPage.css
│   │   │       ├── UserNameSelectPage.tsx
│   │   │       └── UserNameSelectPage.css
│   │   ├── App.tsx
│   │   ├── App.css
│   │   └── index.tsx / index.css      # エントリーポイント
│   ├── package.json
│   └── tsconfig.json
│
├── worker/                             # バックグラウンドタスク実行（非同期処理）
│   ├── __init__.py
│   ├── job_handler.py                  # タスク種別ごとの処理
│   └── worker_runner.py                # 無限ループで待機・実行
│
├── .env                                # バックエンド用環境変数（DynamoDB設定など）
├── requirements.txt                    # Python依存パッケージ一覧
│
├── start_api_server.sh                 # APIサーバー起動
├── start_web_server.sh                 # Webフロント起動（React）
├── start_worker.sh                     # ワーカー起動
├── start_cleanup_tasks.sh              # 古いタスク削除スクリプト実行
│
├── test_aws_client.py                  # AWSクライアントのテスト
├── test_post_attendance.py             # 勤怠登録のテスト
├── test_post_user.py                   # ユーザー登録のテスト
├── test_task_handler.py                # ワーカータスク処理のテスト
└── test_task_queue.py                  # タスクキュー操作のテスト
```

## 開発言語

- Python（バックエンド）
- React（フロントエンド）

## カードリーダーの設定方法

Raspberry Pi 4BのUSBポートにNFCカードリーダー（RC-S380 S）を接続した状態で起動

- カードリーダーを認識しているかを確認
```
$ lsusb

# 出力例
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 003: ID 054c:06c1 Sony Corp. RC-S380/S          # <-NFCカードリーダーが表示されていればOK
Bus 001 Device 002: ID 2109:3431 VIA Labs, Inc. Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub

# nfcpyのインストール
$ sudo pip install nfcpy
```

- nfcpyが適切インストールされているか確認する
```
$ cd ~
$ git clone https://github.com/nfcpy/nfcpy.git
$ sudo python3 nfcpy/examples/tagtool.py show

$ python3 -m nfc

# 出力例
This is the 1.0.4 version of nfcpy run in Python 3.9.x
on Linux-6.1.x-aarch64-with-glibc2.31
I'm now searching your system for contactless devices
** found usb:054c:06c1 at usb:xxx:xxx but access is denied
-- the device is owned by 'root' but you are '***'
-- also members of the 'root' group would be permitted
-- you could use 'sudo' but this is not recommended
-- better assign the device to the 'plugdev' group
   sudo sh -c 'echo SUBSYSTEM=="usb", ACTION=="add", ATTRS{idVendor}=="054c", ATTRS{idProduct}=="06c1", GROUP="plugdev" >> /etc/udev/rules.d/nfcdev.rules'
   sudo udevadm control -R # then re-attach device
I'm not trying serial devices because you haven't told me
-- add the option '--search-tty' to have me looking
-- but beware that this may break other serial devs
Sorry, but I couldn't find any contactless device

# -- better assign the device to the 'plugdev' group以下に記載のコマンドを実行する
# 上記の出力例の場合
$ sudo sh -c 'echo SUBSYSTEM=="usb", ACTION=="add", ATTRS{idVendor}=="054c", ATTRS{idProduct}=="06c1", GROUP="plugdev" >> /etc/udev/rules.d/nfcdev.rules'
$ sudo udevadm control -R # then re-attach device
```