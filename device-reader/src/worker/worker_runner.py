import time
import sys
import os
# プロジェクトルートをモジュール検索パスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.task_queue    import get_next_pending_task, mark_task_done, mark_task_failed
from shared.config        import LOG_PATHS
from shared.error_handler import ErrorHandler
from worker.task_handler  import handle_task

logger = ErrorHandler(log_file=str(LOG_PATHS["worker"]))

def worker_run():
    """ワーカーを起動し，タスクを処理するメインループ"""
    while True:
        # 次のタスクを取得
        task = get_next_pending_task()
        # タスクがない場合は10秒置きにスキップ
        if not task:
            time.sleep(10)
            continue

        # タスクを処理
        try:
            logger.log_info(f"タスク取得: ID={task['id']}, タイプ={task['job_type']}, パラメータ={task['params']}")
            res = handle_task(task)
            # レスポンスエラーの場合ログ出力
            if res["statusCode"] == 200:
                mark_task_done(task["id"])
            else:
                logger.log_error(f"レスポンスエラー: {res['statusCode']}, タスクID={task['id']}")
                mark_task_failed(task["id"])

        except Exception as e:
            mark_task_failed(task["id"])
            logger.log_error(f"タスク失敗: ID={task['id']}, エラー: {e}")

if __name__ == "__main__":
    try:
        logger.log_info("ワーカー起動")
        worker_run()

    except KeyboardInterrupt:
        logger.log_info("ワーカー停止")
        pass
    except Exception as e:
        logger.log_error(f"ワーカーエラー: {e}")
        raise
    finally:
        logger.log_info("ワーカー終了")
        pass