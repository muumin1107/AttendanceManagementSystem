import os
from notion_client import Client
from datetime import datetime, timedelta, timezone
import json
from typing import List, Dict, Any

# 定数の定義
CONFIG_PATH                 = '/home/pi/attendance_system/API/config/config.json'
IDPOOL_COLUMNS_LENGTH       = 4
ATTENDANCE_COLUMNS_LENGTH   = 3
VALID_ATTRIBUTES            = ['ICカード', 'スマートフォン', 'その他']
VALID_STATES                = ['出勤', '休入', '休出', '退勤']
INTERVAL                    = 5
TIMEZONE_JST                = timezone(timedelta(hours=9), 'JST')
STATE_TRANSITIONS = {
    '未登録': ['出勤'],
    '出勤': ['休入', '退勤'],
    '休入': ['休出'],
    '休出': ['休入', '退勤'],
    '退勤': ['出勤']
}

class ConfigError(Exception):
    """設定ファイルやキーに関するエラーを処理する例外クラス"""
    pass

class ConfigLoader:
    """設定ファイルの読み込みとキーの取得を行うクラス"""

    @staticmethod
    def load_config(path: str = CONFIG_PATH) -> dict:
        if not os.path.exists(path):
            raise ConfigError(f'Config file not found: {path}')

        with open(path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        if  'NOTION_ACCESS_TOKEN' not in config['NOTION']   or\
            'NOTION_IDPOOL_ID' not in config['NOTION']      or\
            'NOTION_ATTENDANCE_ID' not in config['NOTION']  or\
            'NOTION_ATTENDANCE_STATE_ID' not in config['NOTION']:
            raise ConfigError("Notion API access token and database ID must be set in config file.")
        return config

class NotionAPIClient:
    """
    Notion APIクライアントを管理し、IDプールと勤怠データベースを操作するクラス
    """

    def __init__(self) -> None:
        """
        Notion APIクライアントの初期化。環境変数からアクセストークンとデータベースIDを取得。

        Raises:
            ValueError: アクセストークンやデータベースIDが設定されていない場合に発生。
        """
        try:
            config = ConfigLoader.load_config()
            self.NOTION_ACCESS_TOKEN        = config['NOTION']['NOTION_ACCESS_TOKEN']
            self.NOTION_IDPOOL_ID           = config['NOTION']['NOTION_IDPOOL_ID']
            self.NOTION_ATTENDANCE_ID       = config['NOTION']['NOTION_ATTENDANCE_ID']
            self.NOTION_ATTENDANCE_STATE_ID = config['NOTION']['NOTION_ATTENDANCE_STATE_ID']

            self.client = Client(auth=self.NOTION_ACCESS_TOKEN)
        except Exception as e:
            raise ValueError(f"-> __init__ {e}")

    def _query_database(self, db_name: str) -> List[Dict[str, Any]]:
        """
        指定されたデータベースからデータを取得する。

        Args:
            db_name (str): 'id' または 'attendance' データベース名を指定。

        Returns:
            list: データベースから取得したクエリ結果。

        Raises:
            ValueError: 不明なデータベース名が指定された場合に発生。
        """
        try:
            if db_name == 'id':
                return self.client.databases.query(database_id=self.NOTION_IDPOOL_ID)['results']
            elif db_name == 'attendance':
                return self.client.databases.query(database_id=self.NOTION_ATTENDANCE_ID)['results']
            elif db_name == 'state':
                return self.client.databases.query(database_id=self.NOTION_ATTENDANCE_STATE_ID)['results']
            else:
                raise ValueError(f"Unknown database name '{db_name}'")
        except Exception as e:
            raise ValueError(f"-> _query_database: {e}")

    def _extract_data(self, db_name: str, db_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        データベースから取得したクエリ結果から必要なカラムデータを抽出する。

        Args:
            db_name (str): 'id' または 'attendance' データベース名を指定。
            db_results (list): データベースから取得したクエリ結果。

        Returns:
            list: 抽出されたデータ。

        Raises:
            ValueError: 不明なデータベース名が指定された場合に発生。
        """
        try:
            if db_name == 'id':
                return [
                    {
                        'id'            : tmp['properties']['ID']['title'][0]['plain_text'],
                        'name'          : tmp['properties']['名前']['rich_text'][0]['plain_text'],
                        'attribute'     : tmp['properties']['属性']['select']['name'],
                        'description'   : tmp['properties']['備考']['rich_text'][0]['plain_text'],
                        'record_id'     : tmp['id']
                    }
                    for tmp in db_results
                ]
            elif db_name == 'attendance':
                return [
                    {
                        'name'          : tmp['properties']['名前']['title'][0]['plain_text'],
                        'next_state'    : tmp['properties']['区分']['select']['name'],
                        'current_time'  : tmp['properties']['時間']['date']['start'],
                        'record_id'     : tmp['id']
                    }
                    for tmp in db_results
                ]
            elif db_name == 'state':
                return [
                    {
                        'name'          : tmp['properties']['名前']['title'][0]['plain_text'],
                        'current_state' : tmp['properties']['区分']['select']['name'],
                        'record_id'     : tmp['id']
                    }
                    for tmp in db_results
                ]
            else:
                raise ValueError(f"Unknown database name: '{db_name}'")
        except Exception as e:
            raise ValueError(f"-> _extract_data: {e}")

    def _filter_data(self, data: List[Dict[str, Any]], filter_name: str) -> List[Dict[str, Any]]:
        """
        データを名前でフィルタリングする。

        Args:
            data (list): データベースから抽出されたデータ。
            filter_name (str): フィルタリングする名前。

        Returns:
            list: フィルタリングされたデータ。
        """
        try:
            if data is None or len(data) == 0:
                return None
            return [tmp for tmp in data if tmp['name'] == filter_name]
        except Exception as e:
            raise ValueError(f"-> _filter_data: {e}")

    def _sort_data(self, data: List[Dict[str, Any]], key: str) -> List[Dict[str, Any]]:
        """
        指定されたキーでデータをソートする。

        Args:
            data (list): ソート対象のデータ。
            key (str): ソートのキー。

        Returns:
            list: ソートされたデータ。

        Raises:
            ValueError: 指定されたキーがデータに存在しない場合に発生。
        """
        try:
            if data is None or len(data) == 0:
                return None
            if key not in data[0].keys():
                raise ValueError(f"Unknown key: {key}")
            return sorted(data, key=lambda x: x[key], reverse=True)
        except Exception as e:
            raise ValueError(f"-> _sort_data: {e}")

    def get_name(self, id: str) -> str:
        """
        IDから対応する名前を取得する。

        Args:
            id (str): 検索するID。

        Returns:
            str: IDに対応する名前。該当しない場合はNone。
        """
        try:
            id_data = self._query_database(db_name='id')
            id_data = self._extract_data(db_name='id', db_results=id_data)
            for tmp in id_data:
                if tmp['id'] == id:
                    return tmp['name']
            return None
        except Exception as e:
            raise ValueError(f"-> get_name {e}")

    def remove_data(self, db_name: str="attendance", name: str="all") -> None:
        """
        指定した名前のデータを削除する。

        Args:
            db_name (str): 'id' または 'attendance' データベース名を指定。
            name (str): 削除対象の名前（全て削除する場合は'all'を指定）。

        Raises:
            ValueError: 不明なデータベース名が指定された場合に発生。
        """
        try:
            data = self._query_database(db_name=db_name)
            data = self._extract_data(db_name=db_name, db_results=data)
            # MEMO: '全て'を指定した場合はフィルタリングしない
            if not(db_name == "attendance" and name == "all"):
                data = self._filter_data(data=data, filter_name=name)
            self._remove_all_data(data)
            # if db_name == 'id':
            #     id_data = self._query_database(db_name='id')
            #     id_data = self._extract_data(db_name='id', db_results=id_data)
            #     id_data = self._filter_data(data=id_data, filter_name=name)
            #     self._remove_all_data(id_data)
            # elif db_name == 'attendance':
            #     attendance_data = self._query_database(db_name='attendance')
            #     attendance_data = self._extract_data(db_name='attendance', db_results=attendance_data)
            #     attendance_data = self._filter_data(data=attendance_data, filter_name=name)
            #     self._remove_all_data(attendance_data)
            # else:
            #     raise ValueError(f"Unknown database name: {db_name}")
        except Exception as e:
            raise ValueError(f"-> remove_data {e}")

    def _remove_all_data(self, data: List[Dict[str, Any]]) -> None:
        """
        指定されたデータを全て削除（アーカイブ）する。

        Args:
            data (list): 削除対象のデータリスト。
        """
        try:
            if data is None or len(data) == 0:
                return None
            for tmp in data:
                self.client.pages.update(page_id=tmp['record_id'], archived=True)
        except Exception as e:
            raise ValueError(f"-> _remove_all_data: {e}")

    def add_data(self, db_name: str, entry_data: Dict[str, Any]) -> None:
        """
        新しいデータをデータベースに追加する。

        Args:
            db_name (str): 'id' または 'attendance' データベース名を指定。
            entry_data (dict): 追加するデータ。

        Raises:
            ValueError: 不明なデータベース名が指定された場合に発生。
        """
        try:
            if db_name == 'id':
                self._add_id_data(entry_data)
            elif db_name == 'attendance':
                self._add_attendance_data(entry_data)
            elif db_name == 'state':
                self._add_state_data(entry_data)
            else:
                raise ValueError(f"Unknown database name '{db_name}'")
        except Exception as e:
            raise ValueError(f"-> add_data {e}")

    def _add_id_data(self, entry_data: Dict[str, Any]) -> None:
        """
        IDプールにデータを追加する。

        Args:
            entry_data (dict): 追加するデータ。
        """
        try:
            self.client.pages.create(
                parent={'database_id': self.NOTION_IDPOOL_ID},
                properties={
                    'ID'        : {'title': [{'text': {'content': entry_data['id']}}]},
                    '名前'      : {'rich_text': [{'text': {'content': entry_data['name']}}]},
                    '属性'      : {'select': {'name': entry_data['attribute']}},
                    '備考'      : {'rich_text': [{'text': {'content': entry_data['description']}}]}
                }
            )
        except Exception as e:
            raise ValueError(f"-> _add_id_data: {e}")

    def _add_attendance_data(self, entry_data: Dict[str, Any]) -> None:
        """
        勤怠データベースにデータを追加する。

        Args:
            entry_data (dict): 追加する勤怠データ。
        """
        try:
            self.client.pages.create(
                parent={'database_id': self.NOTION_ATTENDANCE_ID},
                properties={
                    '名前': {'title' : [{'text': {'content': entry_data['name']}}]},
                    '区分': {'select': {'name': entry_data['next_state']}},
                    '時間': {'date'  : {'start': entry_data['current_time']}}
                }
            )
        except Exception as e:
            raise ValueError(f"-> _add_attendance_data: {e}")

    def _add_state_data(self, entry_data: Dict[str, Any]) -> None:
        """
        勤怠状況データベースにデータを追加する。

        Args:
            entry_data (dict): 追加する状態データ。
        """
        try:
            self.client.pages.create(
                parent={'database_id': self.NOTION_ATTENDANCE_STATE_ID},
                properties={
                    '名前': {'title': [{'text': {'content': entry_data['name']}}]},
                    '区分': {'select': {'name': entry_data['next_state']}},
                    '時間': {'date': {'start': entry_data['current_time']}}
                }
            )
        except Exception as e:
            raise ValueError(f"-> _add_state_data: {e}")

    def update_state_data(self, entry_data: Dict[str, Any], record_id) -> None:
        """
        勤怠状況データベースの状態を更新する。

        Args:
            entry_data (dict): 更新する状態データ。
        """
        try:
            self.client.pages.update(
                page_id=record_id,
                properties={
                    '名前': {'title': [{'text': {'content': entry_data['name']}}]},
                    '区分': {'select': {'name': entry_data['next_state']}},
                    '時間': {'date': {'start': entry_data['current_time']}}
                }
            )
            return True
        except Exception as e:
            raise ValueError(f"-> update_state_data: {e}")

    def get_current_time(self) -> str:
        """
        現在時刻を5分単位で丸めたISOフォーマットの文字列を返す。

        Returns:
            str: 現在時刻を丸めたISOフォーマットの文字列。
        """
        try:
            current_time = datetime.now(TIMEZONE_JST)
            current_time = current_time - timedelta(minutes=current_time.minute % INTERVAL, seconds=current_time.second)
            return current_time.isoformat()
        except Exception as e:
            raise ValueError(f"-> get_current_time: {e}")

    def validate_data(self, db_name: str, entry_data: Dict[str, Any]) -> bool:
        """
        データの整合性を確認する。

        Args:
            db_name (str): 'id' または 'attendance' データベース名を指定。
            entry_data (dict): 整合性を確認するデータ。

        Returns:
            bool: 整合性が正しい場合はTrue、不正な場合はFalse。

        Raises:
            ValueError: 不明なデータベース名が指定された場合に発生。
        """
        try:
            if db_name == 'id':
                return self._validate_id_data(entry_data)
            elif db_name == 'attendance':
                return self._validate_attendance_data(entry_data)
            else:
                raise ValueError(f"Unknown database name '{db_name}'")
        except Exception as e:
            raise ValueError(f"-> validate_data {e}")

    def _validate_id_data(self, entry_data: Dict[str, Any]) -> bool:
        """
        IDデータの整合性を確認する。

        Args:
            entry_data (dict): 整合性を確認するIDデータ。

        Returns:
            bool: 整合性が正しい場合はTrue、不正な場合はFalse。
        """
        try:
            return (
                len(entry_data) == IDPOOL_COLUMNS_LENGTH    and
                len(entry_data['id']) > 0                   and
                isinstance(entry_data['id'], str)           and
                len(entry_data['name']) > 0                 and
                isinstance(entry_data['name'], str)         and
                entry_data['attribute'] in VALID_ATTRIBUTES and
                len(entry_data['description']) > 0          and
                isinstance(entry_data['description'], str)
            )
        except Exception as e:
            raise ValueError(f"-> _validate_id_data: {e}")

    def _validate_attendance_data(self, entry_data: Dict[str, Any]) -> bool:
        """
        勤怠データの整合性を確認する。

        Args:
            entry_data (dict): 整合性を確認する勤怠データ。

        Returns:
            bool: 整合性が正しい場合はTrue、不正な場合はFalse。
        """
        try:
            return (
                len(entry_data) == ATTENDANCE_COLUMNS_LENGTH and
                len(entry_data['name']) > 0                  and
                isinstance(entry_data['name'], str)          and
                entry_data['next_state'] in VALID_STATES
            )
        except Exception as e:
            raise ValueError(f"-> _validate_attendance_data: {e}")

    def check_duplicate_id(self, id: str) -> bool:
        """
        IDの重複を確認する。

        Args:
            id (str): 確認するID。

        Returns:
            bool: 重複している場合はTrue、していない場合はFalse。
        """
        try:
            id_data = self._query_database(db_name='id')
            id_data = self._extract_data(db_name='id', db_results=id_data)
            return any([tmp['id'] == id for tmp in id_data])
        except Exception as e:
            raise ValueError(f"-> check_duplicate_id {e}")

    def _get_latest_state(self, name: str) -> str:
        """
        指定した名前の最新の勤怠状態を取得する。

        Args:
            name (str): 状態を確認する名前。

        Returns:
            str: 最新の状態。該当するデータがない場合は'未登録'を返す。
        """
        try:
            state_data = self._query_database(db_name='state')
            state_data = self._extract_data(db_name='state', db_results=state_data)
            state_data = self._filter_data(data=state_data, filter_name=name)
            if state_data is None or len(state_data) == 0:
                return '未登録', None
            return state_data[0]['current_state'], state_data[0]['record_id']
        except Exception as e:
            raise ValueError(f"-> _get_latest_state {e}")

    def check_valid_state(self, name: str, next_state: str) -> bool:
        """
        指定した名前の状態遷移が正しいか確認する。

        Args:
            name (str): 状態を確認する名前。
            next_state (str): 次に遷移する状態。

        Returns:
            bool: 正しい状態遷移の場合はTrue、不正な場合はFalse。
        """
        try:
            latest_state, record_id = self._get_latest_state(name=name)
            return next_state in STATE_TRANSITIONS[latest_state], record_id
        except Exception as e:
            raise ValueError(f"-> check_valid_state {e}")