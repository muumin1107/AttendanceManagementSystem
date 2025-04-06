import time
from shared.task_queue import get_next_pending_task, mark_task_done, mark_task_failed
from shared.error_handler import ErrorHandler
from shared.config import LOG_PATHS
from worker.job_handler import handle_task

logger = ErrorHandler(log_file=str(LOG_PATHS["worker"]))

def worker_run():
    """ワーカーを起動し，タスクを処理するメインループ"""
    logger.log_info("ワーカー起動")
    while True:
        # 次のタスクを取得
        task = get_next_pending_task()
        # タスクがない場合はスキップ
        if not task:
            time.sleep(2)
            continue

        # タスクを処理
        try:
            handle_task(task)
            mark_task_done(task["id"])

        except Exception as e:
            mark_task_failed(task["id"])
            logger.log_error(f"タスク失敗: ID={task['id']}, エラー: {e}")

if __name__ == "__main__":
    try:
        worker_run()

    except KeyboardInterrupt:
        logger.log_info("ワーカー停止 by Ctrl+C")