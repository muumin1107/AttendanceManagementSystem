import os
import sys
import logging
from datetime import datetime

class ErrorHandler:
    """エラーハンドリングを行うクラス"""
    def __init__(self, log_file:str):
        """ログファイルを指定してエラーハンドラーを初期化"""
        self.log_file = log_file
        # log_fileのパスが存在しない場合は作成
        if not os.path.exists(log_file):
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
        # ログ設定を追加
        logging.basicConfig(
            filename = self.log_file,
            level    = logging.ERROR,
            format   = '%(asctime)s - %(levelname)s - %(message)s',
            encoding = 'utf-8'
        )

    def log_error(self, error:Exception) -> None:
        """エラーをログファイルに書き込む"""
        timestamp     = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_message = f"[{timestamp}] Unexpected Error: {error}"
        logging.error(error_message)

    def handle_error(self, error:Exception) -> None:
        """エラーを処理するメソッド"""
        self.log_error(error)
        sys.exit(1)