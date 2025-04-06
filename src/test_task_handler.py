from worker.task_handler import handle_task

if __name__ == "__main__":
    # # テスト用のタスク
    # task = {
    #     "job_type": "register_user",
    #     "params": {
    #         "id"  : "test_user",
    #         "name": "Test User"
    #     }
    # }
    # # タスクハンドラを実行
    # handle_task(task)

    # テスト用のタスク
    task = {
        "job_type": "register_attendance",
        "params": {
            "id"    : "test_ser",
            "status": "clock_in"
        }
    }
    # タスクハンドラを実行
    res = handle_task(task)
    print(res)