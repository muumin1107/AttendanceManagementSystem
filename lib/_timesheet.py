import json

from datetime import datetime
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
    def add_data(self, entry_data:json) -> None:
        self.client.pages.create(
            **{
                'parent': {'database_id': self.NOTION_DATABASE_ID},
                'properties': {
                    '名前': {'title': [{'text': {'content': entry_data['name']}}]},
                    '区分': {'select': {'name': entry_data['next_state']}},
                    '時間': {'date': {'start': datetime.now().isoformat()}},
                }
            }
        )

    # 名前を指定して勤怠データを削除
    def remove_db_data(self, remove_name:str) -> None:
        db_json = self.client.databases.query(self.NOTION_DATABASE_ID)['results']
        for i in range(len(db_json)):
            if db_json[i]['properties']['名前']['title'][0]['plain_text'] == remove_name:
                self.client.pages.update(
                    **{
                        'page_id': db_json[i]['id'],
                        'archived': True
                    }
                )

    # 整合性を確認
    def check_data(self, entry_data:json) -> bool:
        # エントリーデータの整合性を確認
        check_1 = len(entry_data) == 2
        check_2 = isinstance(entry_data['name'], str)
        check_3 = entry_data['next_state'] in ['出勤', '休入', '休出', '退勤']
        if not all([check_1, check_2, check_3]):
            return False
        # 状態遷移の整合性を確認
        state_transitions = {
            '未登録': ['出勤'],
            '出勤': ['休入', '退勤'],
            '休入': ['休出'],
            '休出': ['休入', '退勤'],
            '退勤': ['出勤']
        }
        db_json       = self._get_db_data(filter_name=entry_data['name'])
        current_state = db_json[0]['state']
        check_4       = entry_data['next_state'] in state_transitions[current_state]
        if not check_4:
            return False
        return True

    # データベースからデータを取得
    def _get_db_data(self, filter_name:str=None) -> list:
        db_json = self.client.databases.query(self.NOTION_DATABASE_ID)['results']
        result = []
        for i in range(len(db_json)):
            name      = db_json[i]['properties']['名前']['title'][0]['plain_text']
            state     = db_json[i]['properties']['区分']['select']['name']
            timestamp = db_json[i]['properties']['時間']['date']['start']
            result.append({'name': name, 'state': state, 'timestamp': timestamp})
        result = sorted(result, key=lambda x: x['timestamp'], reverse=True)
        if filter_name:
            result = [i for i in result if i['name'] == filter_name]
            if len(result) == 0:
                return [{'name': filter_name, 'state': '未登録', 'timestamp': ''}]
            return result
        else:
            return result