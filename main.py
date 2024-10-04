from lib._timesheet import TimeSheet
from lib._idpool import IdPool

# インスタンス生成
timesheet = TimeSheet()
idpool    = IdPool()

def add(name:str, next_state:str):
    entry_data = {'name': name, 'next_state': next_state}
    if timesheet.check_data(entry_data=entry_data):
        timesheet.add_data(entry_data=entry_data)
        print('勤怠データを追加に成功しました')
        return True
    else:
        print('勤怠データの追加に失敗しました')
        return False

def remove(name:str):
    try:
        timesheet.remove_db_data(remove_name=name)
        print('勤怠データを削除に成功しました')
        return True
    except:
        print('勤怠データの削除に失敗しました')
        return False

if __name__ == "__main__":
    add(name='原田海斗', next_state='退勤')
    # remove(name='原田海斗')