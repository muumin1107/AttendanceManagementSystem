from lib._notiontools import NotionTools
from lib._cardreadertools import CardReaderTools

notiontools     = NotionTools()
cardreadertools = CardReaderTools()

# IDプールにID情報を登録
def register_id(id_num:str, name:str, attribute:str, discription:str):
    try:
        if notiontools.add_id(id=id_num, name=name, attribute=attribute, discription=discription):
            return {'code': 200, 'body': 'ID registration completed.'}
        else:
            return {'code': 400, 'body': 'Failed to register ID.'}
    except Exception as e:
            return {'code': 500, 'body': str(e)}

# 勤怠データを登録
def register_attendance(id_num:str, next_state:str):
    try:
        name = notiontools.search_id(id_num=id_num)
        if name:
            if notiontools.add_db(name=name, next_state=next_state):
                return {'code': 200, 'body': 'Attendance registration completed.'}
            else:
                return {'code': 400, 'body': 'Failed to register attendance.'}
        else:
                return {'code': 400, 'body': 'This ID is not registered.'}
    except Exception as e:
                return {'code': 500, 'body': str(e)}

# IDを削除
def remove_data(id_num:str, mode:str, name:str):
    try:
        is_user = notiontools.search_id(id_num=id_num)
        if is_user == name and mode == 'id':
            if notiontools.remove_id(name=name):
                return {'code': 200, 'body': 'ID deletion completed.'}
            else:
                return {'code': 400, 'body': 'Failed to delete ID.'}
        elif is_user == name and mode == 'db':
            if notiontools.remove_db(name=name):
                return {'code': 200, 'body': 'Attendance data deletion completed.'}
            else:
                return {'code': 400, 'body': 'Failed to delete attendance data.'}
        else:
                return {'code': 400, 'body': 'Name is not found. / mode is invalid.'}
    except Exception as e:
                return {'code': 500, 'body': str(e)}

if __name__ == '__main__':
    try:
        print('Please touch the card.')
        id_num = cardreadertools.read_card()
        if id_num:
            print(register_id(id_num=id_num, name='山田太郎', attribute='ICカード', discription='学生証'))
            #print(register_attendance(id_num=id_num, next_state='出勤'))
            #print(remove_data(id_num=id_num, mode='id', name='佐藤花子'))
            #print(remove_data(id_num=id_num, mode='db', name='佐藤花子'))
        else:
            print({'code': 400, 'body': 'ID not found.'})
    except Exception as e:
            print({'code': 500, 'body': str(e)})