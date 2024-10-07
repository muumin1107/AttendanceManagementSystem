from lib._timesheet import TimeSheet
from lib._idpool import IdPool

class NotionTools:
    def __init__(self):
        self.timesheet = TimeSheet()
        self.idpool = IdPool()

    # 勤怠データを追加
    def add_db(self, name: str, next_state: str) -> bool:
        entry_data = {'name': name, 'next_state': next_state}
        try:
            if self.timesheet.check_data(entry_data=entry_data):
                self.timesheet.add_data(entry_data=entry_data)
                print(f"Successfully added timesheet data for {name}.")
                return True
            else:
                print(f"Failed to add timesheet data for {name}: Invalid data.")
                return False
        except Exception as e:
            print(f"Error while adding timesheet data: {e}")
            return False

    # 勤怠データを削除
    def remove_db(self, name: str) -> bool:
        try:
            self.timesheet.remove_db_data(remove_name=name)
            print(f"Successfully removed timesheet data for {name}.")
            return True
        except Exception as e:
            print(f"Error while removing timesheet data: {e}")
            return False

    # IDデータを追加
    def add_id(self, id: str, name: str, attribute: str, description: str) -> bool:
        id_data = {'id_num': id, 'name': name, 'attribute': attribute, 'description': description}
        try:
            if self.idpool.check_id_data(entry_data=id_data):
                self.idpool.add_id_data(entry_data=id_data)
                print(f"Successfully added ID data for {name}.")
                return True
            else:
                print(f"Failed to add ID data for {name}: Invalid data or ID already exists.")
                return False
        except Exception as e:
            print(f"Error while adding ID data: {e}")
            return False

    # IDデータを削除
    def remove_id(self, name: str) -> bool:
        try:
            self.idpool.remove_id_data(remove_name=name)
            print(f"Successfully removed ID data for {name}.")
            return True
        except Exception as e:
            print(f"Error while removing ID data: {e}")
            return False

    # IDを検索して名前を返す
    def search_id(self, id_num: str) -> str:
        try:
            name = self.idpool.search_id_data(id_num=id_num)
            if name:
                print(f"Successfully found name for ID {id_num}: {name}.")
                return name
            else:
                print(f"ID {id_num} not found.")
                return None
        except Exception as e:
            print(f"Error while searching ID data: {e}")
            return None
