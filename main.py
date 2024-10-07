from fastapi import FastAPI, HTTPException, status
from lib._notiontools import NotionTools
from lib._cardreadertools import CardReaderTools

# 定数定義
SUCCESS_CODE = status.HTTP_200_OK
BAD_REQUEST_CODE = status.HTTP_400_BAD_REQUEST
INTERNAL_SERVER_ERROR_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR

# FastAPI アプリケーションのインスタンス
app = FastAPI()

# ツールのインスタンス
notion_tools = NotionTools()
card_reader_tools = CardReaderTools()

# ユーティリティ関数
def encrypt_id(id_num: str) -> str:
    """IDを暗号化する関数"""
    return card_reader_tools.encrypt_uid(uid=id_num)

def handle_error(message: str, code: int):
    """エラーハンドリング用の関数"""
    raise HTTPException(status_code=code, detail=message)

# IDプールにID情報を登録
@app.post('/register_id')
def register_id(id_num: str, name: str, attribute: str, description: str):
    try:
        encrypted_id = encrypt_id(id_num)
        
        if notion_tools.add_id(id=encrypted_id, name=name, attribute=attribute, description=description):
            return {'code': SUCCESS_CODE, 'body': 'ID registration completed.'}
        else:
            handle_error('Failed to register ID.', BAD_REQUEST_CODE)
    except Exception as e:
        handle_error(str(e), INTERNAL_SERVER_ERROR_CODE)

# 勤怠データを登録
@app.post('/register_attendance')
def register_attendance(id_num: str, next_state: str):
    try:
        encrypted_id = encrypt_id(id_num)
        name = notion_tools.search_id(id_num=encrypted_id)
        
        if not name:
            handle_error('This ID is not registered.', BAD_REQUEST_CODE)

        if notion_tools.add_db(name=name, next_state=next_state):
            return {'code': SUCCESS_CODE, 'body': 'Attendance registration completed.'}
        else:
            handle_error('Failed to register attendance.', BAD_REQUEST_CODE)
    except Exception as e:
        handle_error(str(e), INTERNAL_SERVER_ERROR_CODE)

# IDを削除
@app.post('/remove_data')
def remove_data(id_num: str, mode: str, name: str):
    try:
        encrypted_id = encrypt_id(id_num)
        is_user = notion_tools.search_id(id_num=encrypted_id)

        if is_user != name:
            handle_error('Name is not found.', BAD_REQUEST_CODE)

        if mode == 'id':
            if notion_tools.remove_id(name=name):
                return {'code': SUCCESS_CODE, 'body': 'ID deletion completed.'}
            else:
                handle_error('Failed to delete ID.', BAD_REQUEST_CODE)
        elif mode == 'db':
            if notion_tools.remove_db(name=name):
                return {'code': SUCCESS_CODE, 'body': 'Attendance data deletion completed.'}
            else:
                handle_error('Failed to delete attendance data.', BAD_REQUEST_CODE)
        else:
            handle_error('Invalid mode.', BAD_REQUEST_CODE)
    except Exception as e:
        handle_error(str(e), INTERNAL_SERVER_ERROR_CODE)

# ルートエンドポイント
@app.get('/')
def root():
    return {'code': SUCCESS_CODE, 'body': 'Welcome to the API server.'}

# ヘルスチェックエンドポイント
@app.get('/health')
def health():
    return {'code': SUCCESS_CODE, 'body': 'Health check OK.'}