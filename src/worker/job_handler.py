from shared import aws_client

def handle_task(task: dict):
    """タスクハンドラ"""
    # タスクの種類に応じて処理を分岐
    if task["job_type"] == "register_user":
        # ユーザー登録
        aws_client.register_user(**task["params"])
    elif task["job_type"] == "register_attendance":
        # 出席登録
        aws_client.register_attendance(**task["params"])