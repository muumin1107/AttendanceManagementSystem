from lib._timesheet import TimeSheet
from lib._idpool import IdPool

class NotionTools:
    def __init__(self):
        self.timesheet = TimeSheet()
        self.idpool    = IdPool()

    # 勤怠データをDBに追加
    def add_db(self, name: str, next_state: str) -> bool:
        entry_data = {'name': name, 'next_state': next_state}
        if self._is_valid_timesheet_data(entry_data):
            self.timesheet.add_data(entry_data=entry_data)
            return True
        return False

    # 勤怠データを削除
    def remove_db(self, name: str) -> bool:
        self.timesheet.remove_db_data(remove_name=name)
        return True

    # IDをIDプールに追加
    def add_id(self, id: str, name: str, attribute: str, description: str) -> bool:
        id_data = {'id_num': id, 'name': name, 'attribute': attribute, 'description': description}
        if self._is_valid_id_data(id_data):
            self.idpool.add_id_data(entry_data=id_data)
            return True
        return False

    # IDを削除
    def remove_id(self, name: str) -> bool:
        self.idpool.remove_id_data(remove_name=name)
        return True

    # IDを検索
    def search_id(self, id_num: str):
        name = self.idpool.search_id_data(id_num=id_num)
        if name:
            return name
        return None

    # 内部メソッド: Timesheetのデータが有効かどうか確認
    def _is_valid_timesheet_data(self, entry_data: dict) -> bool:
        return self.timesheet.check_data(entry_data=entry_data)

    # 内部メソッド: IDプールのデータが有効かどうか確認
    def _is_valid_id_data(self, id_data: dict) -> bool:
        return self.idpool.check_id_data(entry_data=id_data)