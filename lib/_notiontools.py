from lib._timesheet import TimeSheet
from lib._idpool import IdPool

class NotionTools:
    """Notion関連の操作をまとめたツールクラス"""

    def __init__(self):
        self.timesheet = TimeSheet()
        self.idpool = IdPool()

    # 勤怠データをDBに追加
    def add_db(self, name: str, next_state: str) -> bool:
        """勤怠データをタイムシートに追加"""
        entry_data = {'name': name, 'next_state': next_state}
        
        # データの妥当性を確認
        if self.is_valid_timesheet_data(entry_data):
            try:
                self.timesheet.add_data(entry_data=entry_data)
                return True
            except Exception as e:
                print(f"Error adding timesheet data: {e}")
                return False
        return False

    # 勤怠データを削除
    def remove_db(self, name: str) -> bool:
        """勤怠データをタイムシートから削除"""
        try:
            self.timesheet.remove_db_data(remove_name=name)
            return True
        except Exception as e:
            print(f"Error removing timesheet data: {e}")
            return False

    # IDをIDプールに追加
    def add_id(self, id: str, name: str, attribute: str, description: str) -> bool:
        """IDプールに新しいIDデータを追加"""
        id_data = {'id_num': id, 'name': name, 'attribute': attribute, 'description': description}
        
        # IDデータの妥当性を確認
        if self.is_valid_id_data(id_data):
            try:
                self.idpool.add_id_data(entry_data=id_data)
                return True
            except Exception as e:
                print(f"Error adding ID data: {e}")
                return False
        return False

    # IDを削除
    def remove_id(self, name: str) -> bool:
        """IDプールから指定された名前のIDデータを削除"""
        try:
            self.idpool.remove_id_data(remove_name=name)
            return True
        except Exception as e:
            print(f"Error removing ID data: {e}")
            return False

    # IDを検索
    def search_id(self, id_num: str):
        """ID番号から名前を検索"""
        try:
            name = self.idpool.search_id_data(id_num=id_num)
            return name if name else None
        except Exception as e:
            print(f"Error searching ID: {e}")
            return None

    # 内部メソッド: Timesheetのデータが有効かどうか確認
    def is_valid_timesheet_data(self, entry_data: dict) -> bool:
        """タイムシートデータの妥当性を確認"""
        return self.timesheet.check_data(entry_data=entry_data)

    # 内部メソッド: IDプールのデータが有効かどうか確認
    def is_valid_id_data(self, id_data: dict) -> bool:
        """IDデータの妥当性を確認"""
        return self.idpool.check_id_data(entry_data=id_data)