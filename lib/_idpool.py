import json
import os

from notion_client import Client

class IdPool:
    def __init__(self):
        # 環境変数の取得
        self.NOTION_ACCESS_TOKEN = os.environ.get('NOTION_ACCESS_TOKEN')
        self.NOTION_IDPOOL_ID    = os.environ.get('NOTION_IDPOOL_ID')
        # Notionクライアントの初期化
        self.client              = Client(auth=self.NOTION_ACCESS_TOKEN)

    # IDプールデータを追加
    def add_id_data(self, entry_data:json) -> None:
        self.client.pages.create(
            **{
                'parent': {'database_id': self.NOTION_IDPOOL_ID},
                'properties': {
                    'ID'  : {'title': [{'text': {'content': entry_data['id_num']}}]},
                    '名前': {'rich_text': [{'text': {'content': entry_data['name']}}]},
                    '属性': {'select': {'name': entry_data['attribute']}},
                    '備考': {'rich_text': [{'text': {'content': entry_data['discription']}}]},
                }
            }
        )

    # 名前を指定してIDプールデータを削除
    def remove_id_data(self, remove_name:str) -> None:
        db_json = self.client.databases.query(self.NOTION_IDPOOL_ID)['results']
        for i in range(len(db_json)):
            if db_json[i]['properties']['名前']['rich_text'][0]['plain_text'] == remove_name:
                self.client.pages.update(
                    **{
                        'page_id': db_json[i]['id'],
                        'archived': True
                    }
                )

    # 整合性を確認
    def check_id_data(self, entry_data:json) -> bool:
        # エントリーデータの整合性を確認
        data_check_list = []
        data_check_list.append(len(entry_data) == 4)
        data_check_list.append(isinstance(entry_data['id_num'], str))
        data_check_list.append(isinstance(entry_data['name'], str))
        data_check_list.append(entry_data['attribute'] in ['ICカード', 'スマートフォン', 'その他'])
        data_check_list.append(isinstance(entry_data['discription'], str))
        if not all(data_check_list):
            return False
        # ID重複チェック
        id_data = self._get_id_data()
        if entry_data['id_num'] in [x['id_num'] for x in id_data]:
            return False
        return True

    # ID番号を指定して名前を検索
    def search_id_data(self, id_num:str) -> str:
        id_data = self._get_id_data()
        for i in range(len(id_data)):
            if id_data[i]['id_num'] == id_num:
                return id_data[i]['name']
        return None

    # データベースからデータを取得
    def _get_id_data(self, filter_name:str=None) -> list:
        db_json = self.client.databases.query(self.NOTION_IDPOOL_ID)['results']
        result = []
        for i in range(len(db_json)):
            id_num      = db_json[i]['properties']['ID']['title'][0]['plain_text']
            name        = db_json[i]['properties']['名前']['rich_text'][0]['plain_text']
            attribute   = db_json[i]['properties']['属性']['select']['name']
            discription = db_json[i]['properties']['備考']['rich_text'][0]['plain_text']
            result.append({'id_num': id_num, 'name': name, 'attribute': attribute, 'discription': discription})
        return sorted(result, key=lambda x: x['id_num'], reverse=True)