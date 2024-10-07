from fastapi import FastAPI, HTTPException, status
from lib._notiontools import NotionTools
from lib._cardreadertools import CardReaderTools

app = FastAPI()
notiontools = NotionTools()
cardreadertools = CardReaderTools()

# IDプールにID情報を登録
@app.post('/register_id')
def register_id(id_num: str, name: str, attribute: str, description: str):
    try:
        id_num = cardreadertools.encrypt_uid(uid=id_num)
        if notiontools.add_id(id=id_num, name=name, attribute=attribute, description=description):
            return {'code': status.HTTP_200_OK, 'body': 'ID registration completed.'}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Failed to register ID.')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# 勤怠データを登録
@app.post('/register_attendance')
def register_attendance(id_num: str, next_state: str):
    try:
        id_num = cardreadertools.encrypt_uid(uid=id_num)
        name = notiontools.search_id(id_num=id_num)
        if not name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This ID is not registered.')
        
        if notiontools.add_db(name=name, next_state=next_state):
            return {'code': status.HTTP_200_OK, 'body': 'Attendance registration completed.'}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Failed to register attendance.')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# IDを削除
@app.post('/remove_data')
def remove_data(id_num: str, mode: str, name: str):
    try:
        id_num = cardreadertools.encrypt_uid(uid=id_num)
        is_user = notiontools.search_id(id_num=id_num)
        
        if is_user != name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Name is not found.')

        if mode == 'id':
            if notiontools.remove_id(name=name):
                return {'code': status.HTTP_200_OK, 'body': 'ID deletion completed.'}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Failed to delete ID.')
        elif mode == 'db':
            if notiontools.remove_db(name=name):
                return {'code': status.HTTP_200_OK, 'body': 'Attendance data deletion completed.'}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Failed to delete attendance data.')
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid mode.')

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# ルートエンドポイント
@app.get('/')
def root():
    return {'code': status.HTTP_200_OK, 'body': 'Welcome to the API server.'}

# ヘルスチェックエンドポイント
@app.get('/health')
def health():
    return {'code': status.HTTP_200_OK, 'body': 'Health check OK.'}