from lib._timesheet import TimeSheet
from lib._idpool import IdPool

class NotionTools:
    def __init__(self):
        self.timesheet = TimeSheet()
        self.idpool    = IdPool()

    def add_db(self, name:str, next_state:str):
        entry_data = {'name': name, 'next_state': next_state}
        if self.timesheet.check_data(entry_data=entry_data):
            self.timesheet.add_data(entry_data=entry_data)
            return True
        else:
            return False

    def remove_db(self, name:str):
        self.timesheet.remove_db_data(remove_name=name)
        return True

    def add_id(self, id:str, name:str, attribute:str, discription:str):
        id_data = {'id_num': id, 'name': name, 'attribute': attribute, 'discription': discription}
        if self.idpool.check_id_data(entry_data=id_data):
            self.idpool.add_id_data(entry_data=id_data)
            return True
        else:
            return False

    def remove_id(self, name:str):
        self.idpool.remove_id_data(remove_name=name)
        return True

    def search_id(self, id_num:str):
        name = self.idpool.search_id_data(id_num=id_num)
        if name:
            return name
        else:
            return False