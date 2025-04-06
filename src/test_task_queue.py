from shared.task_queue import enqueue_task, get_next_pending_task, mark_task_done, mark_task_failed

# 1. 次の未処理タスクを取得
task = get_next_pending_task()
if task:
    print(f"取得したタスク: {task}")
    # 2. 任意で完了または失敗にマーク（今回は完了）
    mark_task_done(task["id"])
    print(f"タスク {task['id']} を完了としてマークしました．")
else:
    print("未処理タスクが存在しません．")