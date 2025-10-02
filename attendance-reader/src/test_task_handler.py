from worker.task_handler import handle_task

if __name__ == "__main__":
    # テスト用のタスク
    task = {
        "job_type": "register_user",
        "params": {
            "id"  : "test_id",
            "name": "test_name",
            "grade": "M2"
        }
    }
    # タスクハンドラを実行
    res = handle_task(task)
    print(res)

    # テスト用のタスク
    task = {
        "job_type": "register_attendance",
        "params": {
            "id"    : "test_id",
            "status": "clock_in"
        }
    }
    # タスクハンドラを実行
    res = handle_task(task)
    print(res)