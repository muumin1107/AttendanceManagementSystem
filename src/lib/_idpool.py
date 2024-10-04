import json

from pathlib import Path
from notion_client import Client

class IdPool:
    # 設定ファイルの読み込み
    current_dir = Path(__file__).resolve().parent
    conf_path   = current_dir / '../config/config.json'
    config      = json.load(open(conf_path, 'r', encoding='utf-8'))
    # クラス変数
    NOTION_ACCESS_TOKEN = config['notion']['NOTION_ACCESS_TOKEN']
    NOTION_IDPOOL_ID    = config['notion']['NOTION_IDPOOL_ID']

    def __init__(self):
        self.client = Client(auth=self.NOTION_ACCESS_TOKEN)