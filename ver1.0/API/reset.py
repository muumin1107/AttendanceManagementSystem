from lib._attendancesystemoperation import AttendanceSystemOperation

attendance_system_operation = AttendanceSystemOperation()

if __name__ == '__main__':
    try:
        # 勤怠記録データベースの初期化
        attendance_system_operation.remove_all_attendance()
        # 勤怠状態データベースの初期化
        attendance_system_operation.register_all_attendance(next_state="退勤")
    except Exception as e:
        print(e)