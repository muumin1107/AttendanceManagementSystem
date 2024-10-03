from lib._timesheet import Timesheet

# インスタンス生成
timesheet = Timesheet()

def main():
    result = timesheet.get_all_data()
    print(result)
    return

if __name__ == "__main__":
    main()