import requests

from fastapi import FastAPI
from lib._notiontools import NotionTools
from lib._cardreadertools import CardReaderTools

app             = FastAPI()
notiontools     = NotionTools()
cardreadertools = CardReaderTools()

# IDプールにID情報を登録
@app.post('/register_id')
def register_id(token:str, id_num:str, name:str, attribute:str, discription:str):
    try:
        # result = requests.get(f'https://yleolp2v6n3y2csik6kwvnuioa0zfbik.lambda-url.ap-northeast-1.on.aws/?token={token}').json()
        # if result['result'] == 'valid':
        id_num = cardreadertools.encrypt_uid(uid=id_num)
        if notiontools.add_id(id=id_num, name=name, attribute=attribute, discription=discription):
            return {'code': 200, 'body': 'ID registration completed.'}
        else:
            return {'code': 400, 'body': 'Failed to register ID.'}
        # else:
                # return {'code': 400, 'body': 'Invalid token.'}
    except Exception as e:
                return {'code': 500, 'body': str(e)}

# 勤怠データを登録
@app.post('/register_attendance')
def register_attendance(token:str, id_num:str, next_state:str):
    try:
        # result = requests.get(f'https://yleolp2v6n3y2csik6kwvnuioa0zfbik.lambda-url.ap-northeast-1.on.aws/?token={token}').json()
        # if result['result'] == 'valid':
        id_num = cardreadertools.encrypt_uid(uid=id_num)
        name = notiontools.search_id(id_num=id_num)
        if name:
            if notiontools.add_db(name=name, next_state=next_state):
                return {'code': 200, 'body': 'Attendance registration completed.'}
            else:
                return {'code': 400, 'body': 'Failed to register attendance.'}
        else:
                return {'code': 400, 'body': 'This ID is not registered.'}
        # else:
                    # return {'code': 400, 'body': 'Invalid token.'}
    except Exception as e:
                    return {'code': 500, 'body': str(e)}

# IDを削除
@app.post('/remove_data')
def remove_data(token:str, id_num:str, mode:str, name:str):
    try:
        # result = requests.get(f'https://yleolp2v6n3y2csik6kwvnuioa0zfbik.lambda-url.ap-northeast-1.on.aws/?token={token}').json()
        # if result['result'] == 'valid':
        id_num = cardreadertools.encrypt_uid(uid=id_num)
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
        # else:
                    # return {'code': 400, 'body': 'Invalid token.'}
    except Exception as e:
                    return {'code': 500, 'body': str(e)}

@app.get('/')
def root():
    return {'code': 200, 'body': 'Welcome to the API server.'}

@app.get('/health')
def health():
    return {'code': 200, 'body': 'Health check OK.'}