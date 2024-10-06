import json
import os

from datetime import datetime, timedelta, timezone
# from pathlib import Path
from notion_client import Client

class TimeSheet:
    def __init__(self):
        self.client              = Client(auth=self.NOTION_ACCESS_TOKEN)
        self.NOTION_ACCESS_TOKEN = os.environ.get('NOTION_ACCESS_TOKEN')
        self.NOTION_DATABASE_ID  = os.environ.get('NOTION_DATABASE_ID')

    # 勤怠データを追加
    def add_data(self, entry_data:json) -> None:
        # 現在時刻を取得
        dt = datetime.now(timezone(timedelta(hours=9), 'JST'))
        dt = self._round_to_nearest_minute(dt, time=5)
        self.client.pages.create(
            **{
                'parent': {'database_id': self.NOTION_DATABASE_ID},
                'properties': {
                    '名前': {'title': [{'text': {'content': entry_data['name']}}]},
                    '区分': {'select': {'name': entry_data['next_state']}},
                    '時間': {'date': {'start': dt.isoformat()}},
                }
            }
        )

    # 現在時刻をtime分単位に丸める
    def _round_to_nearest_minute(self, dt:datetime, time:int) -> datetime:
        minutes = (dt.minute // time) * time
        return dt.replace(minute=minutes, second=0, microsecond=0)

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
        data_check_list = []
        data_check_list.append(len(entry_data) == 2)
        data_check_list.append(isinstance(entry_data['name'], str))
        data_check_list.append(entry_data['next_state'] in ['出勤', '休入', '休出', '退勤'])
        if not all(data_check_list):
            return False
        # 状態遷移の整合性を確認
        state_transitions = {
            '未登録': ['出勤'],
            '出勤': ['休入', '退勤'],
            '休入': ['休出'],
            '休出': ['休入', '退勤'],
            '退勤': ['出勤']
        }
        db_json          = self._get_db_data(filter_name=entry_data['name'])
        current_state    = db_json[0]['state']
        state_check_list = []
        state_check_list.append(entry_data['next_state'] in state_transitions[current_state])
        if not all(state_check_list):
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
            result = [x for x in result if x['name'] == filter_name]
            if len(result) == 0:
                return [{'name': filter_name, 'state': '未登録', 'timestamp': ''}]
            return result
        else:
            return result