from shared.aws_client import register_attendance, register_user

if __name__ == "__main__":
    # テストデータ
    test_nfc_id = "test_nfc_id"
    test_name   = "test_name"
    test_status = "clock_out"

    print("ユーザー登録")
    try:
        res = register_user(id=test_nfc_id, name=test_name)
        print(res)
    except Exception as e:
        print(f"ユーザー登録に失敗しました: {e}")

    print("勤怠登録")
    try:
        res = register_attendance(id=test_nfc_id, status=test_status)
        print(res)
    except Exception as e:
        print(f"勤怠登録に失敗しました: {e}")