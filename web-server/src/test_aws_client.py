from shared.aws_client import get_attendance

if __name__ == "__main__":
    print("勤怠情報の取得")
    try:
        res = get_attendance()
        print(res)

    except Exception as e:
        print(f"勤怠情報の取得に失敗しました: {e}")