import json
import os
from datetime import datetime, timedelta, timezone
from notion_client import Client

# 定数化
TIMEZONE_JST = timezone(timedelta(hours=9), 'JST')
VALID_STATES = ['出勤', '休入', '休出', '退勤']
STATE_TRANSITIONS = {
    '未登録': ['出勤'],
    '出勤': ['休入', '退勤'],
    '休入': ['休出'],
    '休出': ['休入', '退勤'],
    '退勤': ['出勤']
}

class TimeSheet:
    def __init__(self):
        # 環境変数の取得
        self.NOTION_ACCESS_TOKEN = os.environ.get('NOTION_ACCESS_TOKEN')
        self.NOTION_DATABASE_ID  = os.environ.get('NOTION_DATABASE_ID')
        # Notionクライアントの初期化
        self.client              = Client(auth=self.NOTION_ACCESS_TOKEN)

    # 勤怠データを追加
    def add_data(self, entry_data: dict) -> None:
        dt = self._get_current_time()
        if not self.check_data(entry_data):
            raise ValueError("Invalid entry data")

        self.client.pages.create(
            parent={'database_id': self.NOTION_DATABASE_ID},
            properties={
                '名前': {'title': [{'text': {'content': entry_data['name']}}]},
                '区分': {'select': {'name': entry_data['next_state']}},
                '時間': {'date': {'start': dt.isoformat()}}
            }
        )

    # 現在時刻を5分単位に丸める
    def _round_to_nearest_minute(self, dt: datetime, interval: int = 5) -> datetime:
        minutes = (dt.minute // interval) * interval
        return dt.replace(minute=minutes, second=0, microsecond=0)

    # 現在の時刻を取得
    def _get_current_time(self) -> datetime:
        return self._round_to_nearest_minute(datetime.now(TIMEZONE_JST))

    # 名前を指定して勤怠データを削除
    def remove_db_data(self, remove_name: str) -> None:
        db_data = self._get_db_data(filter_name=remove_name)
        for record in db_data:
            self.client.pages.update(page_id=record['id'], archived=True)

    # エントリーデータの整合性を確認
    def check_data(self, entry_data: dict) -> bool:
        if not self._validate_entry_data(entry_data):
            return False
        db_data = self._get_db_data(filter_name=entry_data['name'])
        current_state = db_data[0]['state'] if db_data else '未登録'
        return entry_data['next_state'] in STATE_TRANSITIONS.get(current_state, [])

    # エントリーデータの基本整合性をチェック
    def _validate_entry_data(self, entry_data: dict) -> bool:
        return (
            len(entry_data) == 2 and
            isinstance(entry_data['name'], str) and
            entry_data['next_state'] in VALID_STATES
        )

    # データベースからデータを取得
    def _get_db_data(self, filter_name: str = None) -> list:
        db_results = self.client.databases.query(database_id=self.NOTION_DATABASE_ID)['results']
        records = [
            {
                'id': record['id'],
                'name': record['properties']['名前']['title'][0]['plain_text'],
                'state': record['properties']['区分']['select']['name'],
                'timestamp': record['properties']['時間']['date']['start']
            }
            for record in db_results
        ]
        records = sorted(records, key=lambda x: x['timestamp'], reverse=True)
        
        if filter_name:
            filtered_records = [record for record in records if record['name'] == filter_name]
            if not filtered_records:
                return [{'name': filter_name, 'state': '未登録', 'timestamp': ''}]
            return filtered_records
        
        return records