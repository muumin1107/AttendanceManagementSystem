import json

from pathlib import Path
from notion_client import Client

class Timesheet:
    # 設定ファイルの読み込み
    current_dir = Path(__file__).resolve().parent
    conf_path   = current_dir / '../config/config.json'
    config      = json.load(open(conf_path, 'r', encoding='utf-8'))
    # クラス変数
    NOTION_ACCESS_TOKEN = config['notion']['NOTION_ACCESS_TOKEN']
    NOTION_DATABASE_ID  = config['notion']['NOTION_DATABASE_ID']

    def __init__(self):
        self.client = Client(auth=self.NOTION_ACCESS_TOKEN)

    def get_all_data(self) -> list:
        db_json = self.client.databases.query(self.NOTION_DATABASE_ID)['results']
        result  = [self._parse_json(db_json[i]) for i in range(len(db_json))]
        result  = sorted(result, key=lambda x: x['timestamp'], reverse=True)
        return result

    def _parse_json(self, db_json_tmp):
        name      = db_json_tmp['properties']['名前']['title'][0]['plain_text']
        situation = db_json_tmp['properties']['区分']['select']['name']
        timestamp = db_json_tmp['properties']['時間']['date']['start']
        return {'name': name, 'situation': situation, 'timestamp': timestamp}