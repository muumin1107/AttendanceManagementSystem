import json

from pathlib import Path
from notion_client import Client

class TimeSheet:
    # 設定ファイルの読み込み
    current_dir = Path(__file__).resolve().parent
    conf_path   = current_dir / '../config/config.json'
    config      = json.load(open(conf_path, 'r', encoding='utf-8'))

    # クラス変数
    NOTION_ACCESS_TOKEN = config['NOTION_ACCESS_TOKEN']
    NOTION_MASTER_ID    = config['NOTION_DATABASE_ID']

    def __init__(self):
        self.client = Client(auth=self.NOTION_ACCESS_TOKEN)
    
    def get_all_data(self):
        db_json = self.client.databases.query(self.NOTION_MASTER_ID)
        return db_json