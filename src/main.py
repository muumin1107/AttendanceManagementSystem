from lib._timesheet import TimeSheet
from lib._idpool import IdPool

# インスタンス生成
timesheet = TimeSheet()
idpool    = IdPool()

def add_db(name:str, next_state:str):
    entry_data = {'name': name, 'next_state': next_state}
    try:
        if timesheet.check_data(entry_data=entry_data):
            timesheet.add_data(entry_data=entry_data)
            return {"code": 200, "body": "Success"}
        else:
            return {"code": 400, "body": "Bad Request"}
    except Exception as e:
        return {"code": 500, "body": str(e)}

def remove_db(name:str):
    try:
        timesheet.remove_db_data(remove_name=name)
        return {"code": 200, "body": "Success"}
    except Exception as e:
        return {"code": 500, "body": str(e)}

def add_id(id:str, name:str, attribute:str, discription:str):
    id_data = {'id_num': id, 'name': name, 'attribute': attribute, 'discription': discription}
    try:
        if idpool.check_id_data(entry_data=id_data):
            idpool.add_id_data(entry_data=id_data)
            return {"code": 200, "body": "Success"}
        else:
            return {"code": 400, "body": "Bad Request"}
    except Exception as e:
        return {"code": 500, "body": str(e)}

def remove_id(name:str):
    try:
        idpool.remove_id_data(remove_name=name)
        return {"code": 200, "body": "Success"}
    except Exception as e:
        return {"code": 500, "body": str(e)}

def search_id(id_num:str):
    name = idpool.search_id_data(id_num=id_num)
    try:
        if name:
            return {"code": 200, "body": name}
        else:
            return {"code": 200, "body": "Not Found"}
    except Exception as e:
        return {"code": 500, "body": str(e)}

if __name__ == "__main__":
    print(search_id(id_num='NDFYUIKJNBVFY'))
    # print(add_id(id='NDFYUIKJNBVFY', name='原田海斗', attribute='ICカード', discription='ナイスパス'))
    # print(remove_id(name='原田海斗'))
    # print(add_db(name='原田海斗', next_state='出勤'))
    # print(remove_db(name='原田海斗'))