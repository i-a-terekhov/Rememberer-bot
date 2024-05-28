from datetime import datetime


def current_time() -> str:
    curr_time = datetime.now().strftime('%H:%M:%S')
    return curr_time


def current_datatime() -> str:
    curr_time = datetime.now().strftime('%y.%m.%d, %H:%M')
    return curr_time


def parse_datetime(date_string: str) -> datetime:
    """
    Функция принимает строку с датой и временем в формате 'YYYY-MM-DD HH:MM'
    и возвращает объект datetime.
    """
    return datetime.strptime(date_string, '%Y-%m-%d %H:%M')


def datetime_to_string(dt: datetime) -> str:
    """
    Функция принимает объект datetime и возвращает строку с датой и временем
    в формате 'YYYY-MM-DD HH:MM'.
    """
    return dt.strftime('%Y-%m-%d %H:%M')
