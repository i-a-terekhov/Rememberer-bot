from datetime import datetime


def current_time() -> str:
    curr_time = datetime.now().strftime('%H:%M:%S')
    return curr_time


def current_datatime() -> str:
    curr_time = datetime.now().strftime('%y.%m.%d, %H:%M')
    return curr_time

