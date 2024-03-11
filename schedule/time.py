from datetime import datetime


def current_time() -> str:
    curr_time = datetime.now().strftime('%H:%M:%S')
    return curr_time

