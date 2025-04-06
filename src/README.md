# 【Raspberry Pi】カードリーダー式在籍確認システム

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
│   │   └── user.py                     # ユーザー情報用スキーマ
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
