# 【Raspberry Pi】カードリーダー式在籍確認システム（web-server）

## システム環境

- Raspberry Pi 4B（device-reader）

| Raspberry Pi Imager | OS                               | Kernel     |
----                  |----                              |----
| v1.8.5              | Raspbian GNU/Linux 11 (bullseye) | 6.1.21-v8+ |

- FastAPI（ローカルAPIサーバー）

## プロジェクト構成

```
.
├── app/                                # アプリケーション本体
│   ├── __init__.py
│   ├── main.py                         # FastAPI アプリのエントリーポイント
│   └── api/                            # API ルーティング定義
│       ├── __init__.py
│       └── attendance.py               # 勤怠情報取得用APIエンドポイント
│
├── shared/                             # 共通処理・ユーティリティ
│   ├── __init__.py
│   ├── api_client.py                   # ローカルAPI呼び出し用クライアント
│   ├── aws_client.py                   # AWSへのアクセス処理
│   ├── codec.py                        # エンコード・デコード関連
│   ├── config.py                       # 環境設定や定数の管理
│   └── error_handler.py                # エラー処理共通ロジック
│
├── logs/                               # ログファイル出力ディレクトリ
│
├── .env                                # 環境変数定義ファイル
├── requirements.txt                    # Python依存パッケージ一覧
├── start_api_server.sh                 # APIサーバー起動スクリプト
│
├── test_aws_client.py                  # AWSクライアントのテスト
└── test_get_attendance.py              # 勤怠情報取得APIのテスト
```