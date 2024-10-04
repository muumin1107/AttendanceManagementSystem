from lib._timesheet import TimeSheet
from lib._idpool import IdPool

class NotionAPI:

    def __init__(self):
        self.timesheet = TimeSheet()
        self.idpool    = IdPool()

    def add_db(self, name:str, next_state:str):
        entry_data = {'name': name, 'next_state': next_state}
        try:
            if self.timesheet.check_data(entry_data=entry_data):
                self.timesheet.add_data(entry_data=entry_data)
                return {"code": 200, "body": "Success"}
            else:
                return {"code": 400, "body": "Bad Request"}
        except Exception as e:
            return {"code": 500, "body": str(e)}

    def remove_db(self, name:str):
        try:
            self.timesheet.remove_db_data(remove_name=name)
            return {"code": 200, "body": "Success"}
        except Exception as e:
            return {"code": 500, "body": str(e)}

    def add_id(self, id:str, name:str, attribute:str, discription:str):
        id_data = {'id_num': id, 'name': name, 'attribute': attribute, 'discription': discription}
        try:
            if self.idpool.check_id_data(entry_data=id_data):
                self.idpool.add_id_data(entry_data=id_data)
                return {"code": 200, "body": "Success"}
            else:
                return {"code": 400, "body": "Bad Request"}
        except Exception as e:
            return {"code": 500, "body": str(e)}

    def remove_id(self, name:str):
        try:
            self.idpool.remove_id_data(remove_name=name)
            return {"code": 200, "body": "Success"}
        except Exception as e:
            return {"code": 500, "body": str(e)}

    def search_id(self, id_num:str):
        name = self.idpool.search_id_data(id_num=id_num)
        try:
            if name:
                return {"code": 200, "body": name}
            else:
                return {"code": 200, "body": "Not Found"}
        except Exception as e:
            return {"code": 500, "body": str(e)}