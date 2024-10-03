from lib._timesheet import Timesheet

# インスタンス生成
timesheet = Timesheet()

def main():
    timesheet.add_data('山田太郎', '出勤', '2021-09-01T09:00:00Z')
    return

if __name__ == "__main__":
    main()