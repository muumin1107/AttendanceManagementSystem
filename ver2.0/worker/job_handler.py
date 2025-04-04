from shared import aws_client

def handle_task(task: dict):
    """タスクハンドラ"""
    if task["job_type"] == "register_user":
        aws_client.register_user(**task["params"])
    elif task["job_type"] == "register_attendance":
        aws_client.register_attendance(**task["params"])