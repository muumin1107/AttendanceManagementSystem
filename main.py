from lib._timesheet import Timesheet

# インスタンス生成
timesheet = Timesheet()

def main(name:str, next_state:str):
    entry_data = {'name': name, 'next_state': next_state}
    if timesheet.check_data(entry_data=entry_data):
        timesheet.add_data(entry_data=entry_data)
        return True
    else:
        return False

if __name__ == "__main__":
    flag = main(name='山田太郎', next_state='退勤') # 例: {'name': '原田海斗', 'state': '出勤'}
    if flag:
        print('勤怠データを登録に成功しました')
    else:
        print('勤怠データの登録に失敗しました')