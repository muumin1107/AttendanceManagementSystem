# 【Raspberry Pi】カードリーダー式在籍確認システム

## システム概要図

![システム概要図](documents/システム概要図.png)

## システム環境

- Raspberry Pi 4B（ローカルサーバー）

| Raspberry Pi Imager | OS                               | Kernel     |
----                  |----                              |----
| v1.8.5              | Raspbian GNU/Linux 11 (bullseye) | 6.1.21-v8+ |

- FastAPI（ローカルAPIサーバー）
- SQLite（バッファ）
- RC-S380 S（カードリーダー）
- AWS Cloud（クラウドサーバー）

| APIサーバー          | データベース | アクセス制限 | 監視       |
----                  |----         |----         |----
| API Gateway, Lambda | DynamoDB    | IAM, WAF    | CloudWatch |

## プロジェクト構成

```bash
.
├── app/                                # アプリケーション本体
│   ├── __init__.py
│   ├── main.py                         # FastAPIアプリ起動エントリーポイント
│   ├── api/                            # APIルーティング定義
│   │   ├── __init__.py
│   │   ├── attendance.py               # 勤怠登録API
│   │   ├── card.py                     # NFCカード読み取りAPI
│   │   └── user.py                     # ユーザー登録API
│   ├── hardware/                       # ハードウェア制御
│   │   └── card_reader.py              # NFCカードリーダー操作
│   ├── schemas/                        # Pydanticスキーマ定義
│   │   ├── __init__.py
│   │   ├── attendance.py               # 勤怠データ用スキーマ
│   │   └── user.py                      # ユーザー情報用スキーマ
│   └── services/                       # アプリケーションロジック
│       └── card_service.py             # カードサービスの処理
│
├── data/                               # データベース関連
│   ├── .init_db.py                     # SQLite初期化スクリプト
│   └── tasks.db                        # タスクキュー用SQLiteデータベース
│
├── logs/                               # ログファイル出力用（空ディレクトリ）
│
├── shared/                             # 共通モジュール
│   ├── __init__.py
│   ├── api_client.py                   # ローカルAPI呼び出しクライアント
│   ├── aws_client.py                   # AWS APIクライアント
│   ├── codec.py                        # データ変換・エンコード処理
│   ├── config.py                       # 環境設定管理
│   ├── error_handler.py                # 例外・エラー処理
│   └── task_queue.py                   # タスクキューの操作（enqueue / dequeue）
│
├── web/                                # Web UI（未実装）
│   └── (未実装)
│
├── worker/                             # バックグラウンド処理（ワーカー）
│   ├── __init__.py
│   ├── job_handler.py                  # 各タスク種別の処理定義
│   └── worker_runner.py                # ワーカープロセスの起動とループ
│
├── .env                                # 環境変数定義ファイル
├── requirements.txt                    # 必要なPythonパッケージ
├── start_api_server.sh                 # APIサーバー起動用スクリプト
├── start_web_server.sh                 # Webサーバー起動用スクリプト
├── start_worker.sh                     # ワーカースクリプト起動用
│
├── test_aws_client.py                  # AWSクライアントのユニットテスト
├── test_post_attendance.py             # 勤怠API POSTのテスト
├── test_post_user.py                   # ユーザー登録APIのテスト
└── test_task_queue.py                  # タスクキュー関連のテスト
```

## 開発言語

- Python（バックエンド）
- React（フロントエンド）

## 仕様定義

- 「NFCカードID」と「ユーザー名」を登録可能
- 同一ユーザーで複数のNFCカードIDを登録可能
- 同一NFCカードIDで複数のユーザーは登録不可能
- 登録済みNFCカードIDで在籍情報を登録可能
- 在籍情報は「出勤」「休入」「休出」「退勤」の4つ
- 在籍情報の変更時に現在籍情報は考慮しない
- 毎日AM0:00に全ユーザーの在籍情報が「退勤」にリセット

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