from lib._notionapiclient import NotionAPIClient
from typing import Union

class AttendanceSystemOperation:
    """
    勤怠システム操作を管理するクラス。Notion APIを介してIDプールと勤怠データの管理を行う。
    """

    def __init__(self) -> None:
        """
        Notion APIクライアントの初期化。
        """
        self.notion_api_client = NotionAPIClient()

    def _verify_id_and_name(self, id: str, name: str) -> Union[str, bool]:
        """
        指定されたIDと名前が一致するか確認するための内部関数。

        Args:
            id (str): 確認するID。
            name (str): 確認する名前。

        Returns:
            str: エラーメッセージが発生した場合。
            bool: 一致している場合はTrue。
        """
        try:
            name_by_id = self.notion_api_client.get_name(id=id)
            if name_by_id is None:
                return 'ID not found'
            if name_by_id != name:
                return 'ID and name do not match'
            return True
        except Exception as e:
            return f"-> _verify_id_and_name: {e}"

    def register_id(self, id: str, name: str, attribute: str, description: str) -> Union[str, bool]:
        """
        IDプールに新しいIDを登録する。

        Args:
            id (str): 登録するID。
            name (str): ユーザーの名前。
            attribute (str): ユーザーの属性（例: ICカード, スマートフォン）。
            description (str): 備考。

        Returns:
            Union[str, bool]: エラーが発生した場合はエラーメッセージ。正常に登録された場合はTrue。
        """
        try:
            entry_data = {
                'id': id,
                'name': name,
                'attribute': attribute,
                'description': description
            }
            # データが有効かどうかを検証
            if not self.notion_api_client.validate_data(db_name='id', entry_data=entry_data):
                return 'Invalid entry data'
            
            # IDが重複していないか確認
            if self.notion_api_client.check_duplicate_id(id=id):
                return 'Duplicate ID'
            
            # データをNotion APIに追加
            self.notion_api_client.add_data(db_name='id', entry_data=entry_data)
            return True
        except Exception as e:
            return f"register_id: {e}"

    def remove_id(self, id: str, name: str) -> Union[str, bool]:
        """
        IDプールから指定されたIDを削除する。

        Args:
            id (str): 削除するID。
            name (str): 削除対象の名前。

        Returns:
            Union[str, bool]: エラーが発生した場合はエラーメッセージ。正常に削除された場合はTrue。
        """
        try:
            verification_result = self._verify_id_and_name(id=id, name=name)
            if verification_result is not True:
                return verification_result
            
            # データベースからデータを削除
            self.notion_api_client.remove_data(db_name='id', name=name)
            return True
        except Exception as e:
            return f"remove_id: {e}"

    def register_attendance(self, id: str, next_state: str) -> Union[str, bool]:
        """
        勤怠データベースに勤怠状態を登録する。

        Args:
            id (str): 登録するユーザーのID。
            next_state (str): 次の状態（例: 出勤, 退勤）。

        Returns:
            Union[str, bool]: エラーが発生した場合はエラーメッセージ。正常に登録された場合はTrue。
        """
        try:
            # IDから名前を取得
            name_by_id = self.notion_api_client.get_name(id=id)
            if name_by_id is None:
                return 'ID not found'

            # 勤怠データを作成
            entry_data = {
                'name': name_by_id,
                'next_state': next_state,
                'current_time': self.notion_api_client.get_current_time()
            }

            # データの検証
            if not self.notion_api_client.validate_data(db_name='attendance', entry_data=entry_data):
                return 'Invalid entry data'
            
            # 状態遷移が有効かどうかをチェック
            if not self.notion_api_client.check_valid_state(name=name_by_id, next_state=next_state):
                return 'Invalid next state'

            # 勤怠データベースにデータを追加
            self.notion_api_client.add_data(db_name='attendance', entry_data=entry_data)
            return True
        except Exception as e:
            return f"register_attendance {e}"

    def remove_attendance(self, id: str, name: str) -> Union[str, bool]:
        """
        勤怠データベースから指定したユーザーの勤怠データを削除する。

        Args:
            id (str): 削除するユーザーのID。
            name (str): ユーザーの名前。

        Returns:
            Union[str, bool]: エラーが発生した場合はエラーメッセージ。正常に削除された場合はTrue。
        """
        try:
            verification_result = self._verify_id_and_name(id=id, name=name)
            if verification_result is not True:
                return verification_result
            
            # 勤怠データベースからデータを削除
            self.notion_api_client.remove_data(db_name='attendance', name=name)
            return True
        except Exception as e:
            return f"remove_attendance {e}"