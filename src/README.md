# 【Raspberry Pi】カードリーダー式在籍確認システム

## プロジェクト構成

```bash
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
│   ├─ ...
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
├── web/                                # フロントエンド（React + TypeScript）
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
