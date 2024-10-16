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
    """勤怠管理を行うクラス"""

    def __init__(self):
        """クラス初期化、環境変数からAPIキーを取得"""
        self.NOTION_ACCESS_TOKEN = os.environ.get('NOTION_ACCESS_TOKEN')
        self.NOTION_DATABASE_ID  = os.environ.get('NOTION_DATABASE_ID')

        if not self.NOTION_ACCESS_TOKEN or not self.NOTION_DATABASE_ID:
            raise ValueError("Notion API access token and database ID must be set in the environment variables.")

        self.client = Client(auth=self.NOTION_ACCESS_TOKEN)

    # 勤怠データを追加
    def add_data(self, entry_data: dict) -> None:
        """エントリーデータをNotionデータベースに追加"""
        current_time = self._get_current_time()

        if not self.check_data(entry_data):
            raise ValueError("Invalid entry data")

        try:
            self.client.pages.create(
                parent={'database_id': self.NOTION_DATABASE_ID},
                properties={
                    '名前': {'title': [{'text': {'content': entry_data['name']}}]},
                    '区分': {'select': {'name': entry_data['next_state']}},
                    '時間': {'date': {'start': current_time.isoformat()}}
                }
            )
        except Exception as e:
            raise ValueError(f"Error adding data to database: {e}")

    # 名前を指定して勤怠データを削除
    def remove_db_data(self, remove_name: str) -> None:
        """指定された名前の勤怠データをNotionから削除"""
        db_data = self._get_db_data(filter_name=remove_name)
        try:
            for record in db_data:
                self.client.pages.update(page_id=record['id'], archived=True)
        except Exception as e:
            raise ValueError(f"Error removing data: {e}")

    # エントリーデータの整合性を確認
    def check_data(self, entry_data: dict) -> bool:
        """エントリーデータの整合性をチェックし、有効な遷移かを確認"""
        if not self._validate_entry_data(entry_data):
            return False

        db_data = self._get_db_data(filter_name=entry_data['name'])
        current_state = db_data[0]['state'] if db_data else '未登録'
        # 次の状態が遷移可能か確認
        return entry_data['next_state'] in STATE_TRANSITIONS.get(current_state, [])

    # エントリーデータの基本整合性をチェック
    def _validate_entry_data(self, entry_data: dict) -> bool:
        """エントリーデータの基本整合性を確認"""
        is_valid_length = len(entry_data) == 2
        is_valid_name = isinstance(entry_data['name'], str)
        is_valid_state = entry_data['next_state'] in VALID_STATES
        return is_valid_length and is_valid_name and is_valid_state

    # データベースからデータを取得
    def _get_db_data(self, filter_name: str = None) -> list:
        """Notionデータベースから勤怠データを取得"""
        try:
            db_results = self.client.databases.query(database_id=self.NOTION_DATABASE_ID)['results']
        except Exception as e:
            raise ValueError(f"Error querying database: {e}")

        # データの整形
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

        # 名前によるフィルタリング
        if filter_name:
            filtered_records = [record for record in records if record['name'] == filter_name]
            if not filtered_records:
                return [{'name': filter_name, 'state': '未登録', 'timestamp': ''}]
            return filtered_records
        return records

    # 現在の時刻を取得
    def _get_current_time(self) -> datetime:
        """現在の時刻を取得し、5分単位で丸める"""
        return self._round_to_nearest_minute(datetime.now(TIMEZONE_JST))

    # 現在時刻を5分単位に丸める
    def _round_to_nearest_minute(self, dt: datetime, interval: int = 5) -> datetime:
        """現在時刻を指定の分単位に丸める"""
        minutes = (dt.minute // interval) * interval
        return dt.replace(minute=minutes, second=0, microsecond=0)