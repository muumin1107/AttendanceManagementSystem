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

    # 勤怠データを追加
    def add_data(self, name:str, situation:str, timestamp:str) -> None:
        if self._check_data(name, situation, timestamp):
            print('データを追加します')
        return

    # データの整合性を確認
    def _check_data(self, name:str, situation:str, timestamp:str) -> bool:
        result = self._get_all_data()
        return True

    # データベースから全データを取得
    def _get_all_data(self) -> list:
        db_json = self.client.databases.query(self.NOTION_DATABASE_ID)['results']
        result = []
        for i in range(len(db_json)):
            name      = db_json[i]['properties']['名前']['title'][0]['plain_text']
            situation = db_json[i]['properties']['区分']['select']['name']
            timestamp = db_json[i]['properties']['時間']['date']['start']
            result.append({'name': name, 'situation': situation, 'timestamp': timestamp})
        return sorted(result, key=lambda x: x['timestamp'], reverse=True)