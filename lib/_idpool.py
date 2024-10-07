import json
import os
from notion_client import Client

# 定数の定義
VALID_ATTRIBUTES = ['ICカード', 'スマートフォン', 'その他']

class IdPool:
    """IDプールを管理するクラス"""
    
    def __init__(self):
        # 環境変数の取得
        self.NOTION_ACCESS_TOKEN = os.environ.get('NOTION_ACCESS_TOKEN')
        self.NOTION_IDPOOL_ID    = os.environ.get('NOTION_IDPOOL_ID')
        # Notionクライアントの初期化
        self.client              = Client(auth=self.NOTION_ACCESS_TOKEN)

    # IDプールデータを追加
    def add_id_data(self, entry_data: dict) -> None:
        """IDプールに新しいデータを追加"""
        if not self.check_id_data(entry_data):
            raise ValueError("Invalid entry data")

        # データ追加処理
        self.client.pages.create(
            parent={'database_id': self.NOTION_IDPOOL_ID},
            properties={
                'ID'  : {'title': [{'text': {'content': entry_data['id_num']}}]},
                '名前': {'rich_text': [{'text': {'content': entry_data['name']}}]},
                '属性': {'select': {'name': entry_data['attribute']}},
                '備考': {'rich_text': [{'text': {'content': entry_data['description']}}]},
            }
        )

    # 名前を指定してIDプールデータを削除
    def remove_id_data(self, remove_name: str) -> None:
        """指定された名前のIDデータを削除"""
        db_json = self._get_id_data(filter_name=remove_name)
        for record in db_json:
            if record['name'] == remove_name:
                self.client.pages.update(
                    page_id=record['id'],
                    archived=True
                )

    # 整合性を確認
    def check_id_data(self, entry_data: dict) -> bool:
        """IDデータの整合性を確認"""
        if not (
            len(entry_data) == 4 and
            isinstance(entry_data['id_num'], str) and
            isinstance(entry_data['name'], str) and
            entry_data['attribute'] in VALID_ATTRIBUTES and
            isinstance(entry_data['description'], str)
        ):
            return False

        # ID重複チェック
        id_data = self._get_id_data()
        if entry_data['id_num'] in [x['id_num'] for x in id_data]:
            return False

        return True

    # ID番号を指定して名前を検索
    def search_id_data(self, id_num: str) -> str:
        """ID番号から名前を検索"""
        id_data = self._get_id_data()
        for record in id_data:
            if record['id_num'] == id_num:
                return record['name']
        return None

    # データベースからデータを取得
    def _get_id_data(self, filter_name: str = None) -> list:
        """NotionデータベースからIDデータを取得"""
        db_results = self.client.databases.query(database_id=self.NOTION_IDPOOL_ID)['results']

        # データの抽出
        result = [
            {
                'id_num': record['properties']['ID']['title'][0]['plain_text'],
                'name': record['properties']['名前']['rich_text'][0]['plain_text'],
                'attribute': record['properties']['属性']['select']['name'],
                'description': record['properties']['備考']['rich_text'][0]['plain_text'],
                'id': record['id']
            }
            for record in db_results
        ]

        # 名前によるフィルタリング
        if filter_name:
            result = [record for record in result if record['name'] == filter_name]
            if not result:
                return [{'name': filter_name, 'state': '未登録', 'id_num': ''}]
        
        # データをID順にソートして返す
        return sorted(result, key=lambda x: x['id_num'], reverse=True)