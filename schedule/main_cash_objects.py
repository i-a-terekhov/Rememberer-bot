import re
from pprint import pprint
from random import randint, choice

from aiogram.types import Message

from schedule.time import current_datatime
from database import kvazi_db
from hidden.tokenfile import OWNER_CHAT_ID


# class UserType:
#     users = kvazi_db.users

    # def __init__(self, message: Message):
    #     self.telegram_id = str(message.from_user.id)
    #     UserType.users.add(self.telegram_id)
    #     print('Множество в классе UserType: ', UserType.users)

    # @classmethod
    # def save_to_bd(cls):
    #     kvazi_db.users.update(cls.users)
    #     print(f'Квази-база после сохранения юзеров из класса:')
    #     pprint(kvazi_db.users)


# class ConfigurateType:
#     users_and_roles = kvazi_db.users_and_roles

    # def __init__(self, room_name: str, message: Message, role: str):
    #     if role not in ['owner', 'admin', 'user']:
    #         raise ValueError("Role must be one of: 'owner', 'admin', 'user'")
    #     configurate = str(message.from_user.id) + '_in_' + room_name
    #     ConfigurateType.users_and_roles[configurate] = {
    #         'telegram_id': str(message.from_user.id),
    #         'nickname': message.from_user.username,
    #         'room': room_name,
    #         'role': role
    #     }

    # @classmethod
    # def save_to_bd(cls):
    #     kvazi_db.users_and_roles.update(cls.users_and_roles)
    #     print(f'Квази-база после сохранения конфигураций из класса:')
    #     pprint(kvazi_db.users_and_roles)


# class RoomType:
#     rooms_settings = kvazi_db.rooms_settings

    # def __init__(self, room_name: str, message: Message):
    #     user_id = str(message.from_user.id)
    #     RoomType.rooms_settings[room_name] = {
    #         'name': room_name,
    #         'owner': user_id,
    #         'admins': [user_id],
    #         'members': [user_id],
    #         'password': message.text,
    #         'rights_to_create_task': 'owner'
    #     }

    # @classmethod
    # def is_room_exist(cls, room_name: str):
    #     if room_name in cls.rooms_settings:
    #         return True
    #     else:
    #         return False

    # @classmethod
    # def is_password_correct(cls, room_name, password):
    #     if cls.rooms_settings[room_name]['password'] == password:
    #         return True
    #     else:
    #         return False

    # @classmethod
    # def save_to_bd(cls):
    #     kvazi_db.rooms_settings.update(cls.rooms_settings)
    #     print(f'Квази-база после сохранения комнат из класса:')
    #     pprint(kvazi_db.rooms_settings)


class TimeToMail:
    """
    Класс для создания словаря временных рассылок timestamps_for_standard_mailings
    """

    print(f'{current_datatime()}: Получаем текущую версию timestamps из kvazi_db в переменную')
    timestamps = kvazi_db.timestamps_for_standard_mailings

class TasksCash:
    """
    Класс для создания буфера БД и работы с ним.
    При объявлении класса создается ссылка all_tasks на словарь из модуля kvazi_bd. Сом словарь из kvazi_bd
    формируется и сохраняется в БД методами, определенными в kvazi_bd.
    Классовые методы позволят работать с информацией в словаре (обновлять, редактировать).
    """

    print(f'{current_datatime()}: Получаем текущую версию БД из kvazi_db в переменную')
    all_tasks = kvazi_db.all_tasks

    @classmethod
    def _make_unic_number_for_task(cls) -> str:
        """
        Внутренняя функция для генерации случайного числа задания, не совпадающего с имеющимися
        """
        while True:
            number = str(randint(1, 10000))
            if number in cls.all_tasks.keys():
                continue
            else:
                return str(number)

    @classmethod
    def check_task(cls, some_task: dict) -> bool:
        """
        Функция проверяет входящий словарь на соответствие формату буфера БД
        """
        # Эталонная запись
        one = {
            'number': '',
            'recipient_id': 0,
            'nickname': '',
            'room': '',
            'text': '',
            'author': '',
            'executor': 0,
            'create_time': '2023-12-10 14:30',
            'period_of_remind': '30:00',
            'execution_level': 0.0,
            'accept_by_author': False,
            'accept_in_time': '2023-12-10 15:30',
            'livetime_after_ending': '12:00',
        }

        if set(some_task.keys()) != set(one.keys()):
            return False

        for key, value in some_task.items():
            if key in ('recipient_id', 'executor'):
                if not isinstance(value, int):
                    return False
            elif key in ('number', 'nickname', 'room', 'text', 'author'):
                if not isinstance(value, str):
                    return False
            elif key in ('create_time', 'accept_in_time'):
                if not isinstance(value, str):
                    return False
                if not re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$', value):
                    return False
            elif key in ('period_of_remind', 'livetime_after_ending'):
                if not isinstance(value, str):
                    return False
                if not re.match(r'^\d{2}:\d{2}$', value):
                    return False
            elif key == 'execution_level':
                if not isinstance(value, float) or value < 0 or value > 1:
                    return False
            elif key == 'accept_by_author':
                if not isinstance(value, bool):
                    return False
            else:
                # Неизвестный ключ
                return False
        print(f'{current_datatime()}: Проверка пройдена! В буфер БД добавлена новая задача.')
        return True

    @classmethod
    def generate_some_tasks(cls, number_of_tasks: int = 10):
        """
        Функция добавляет в буфер БД несколько случайных задач
        """
        recipients = {231423: 'Вася', 231424: 'Петя', 231425: 'Ваня', 231426: 'Толя', OWNER_CHAT_ID: 'Создатель'}
        rooms = ['Первая комната', 'Красная комната', 'Пятая комната', 'Комната 101', 'Тайная комната',
                 'Секретная комната']
        tasks = ['Постирать носки', 'Купить хлеб', 'Заточить ножи', 'Скачать торрент', 'Пройти курс Python',
                 'Принять душ']

        for i in range(number_of_tasks):
            number = cls._make_unic_number_for_task()
            recipient_id = choice(list(recipients.keys()))
            some_task = {
                'number': number,
                'recipient_id': recipient_id,  # получатель уведомления (в данной структуре всегда один)
                'nickname': recipients[recipient_id],
                'room': choice(rooms),  # откуда пришла задача
                'text': choice(tasks),
                'author': recipients[choice(list(recipients.keys()))],  # автор задачи, который подтверждает завершение
                'executor': choice(list(recipients.keys())),
                # участник, ответственный за завершение (может быть только один)
                'create_time': '2023-12-10 14:30',
                'period_of_remind': '30:00',
                'execution_level': randint(0, 100) / 100,
                'accept_by_author': False,
                'accept_in_time': '2023-12-10 15:30',
                'livetime_after_ending': '12:00',
            }
            cls.save_task(new_task=some_task)

    @classmethod
    def save_task(cls, new_task: dict) -> None:
        """
        Функция сохраняет в буфер задачу
        """
        if cls.check_task(new_task):
            number = TasksCash._make_unic_number_for_task()
            TasksCash.all_tasks[number] = new_task

    @classmethod
    def _iter_tasks(cls) -> dict:
        """
        Генератор, возвращающий по одной задаче за раз из буфера БД all_tasks
        """
        for task in cls.all_tasks:
            yield cls.all_tasks[task]

    @classmethod
    def get_mails(cls) -> dict:
        """
        Метод формирует словарь addressee для рассылки сообщений пользователю с группировкой по группам
        """

        # Шаблон словаря для рассылки:
        # addressee = {
        #     'room_id': {
        #         '12213134': ['task', 'task2', 'task3'],
        #         '23452456': ['task'],
        #                 },
        #     'room2_id': {
        #         '23452456': ['task3', 'task2']
        #                 }
        #             }

        addressee = {}
        for task_num, task in cls.all_tasks.items():
            executor = task['executor']
            room = task['room']
            if room in addressee:
                if executor not in addressee[room]:
                    addressee[room][executor] = [task_num]
                else:
                    addressee[room][executor].append(task_num)
            else:
                addressee[room] = {executor: [task_num]}
        print(f'{current_datatime()}: Сформированный словарь рассылок с группировкой по группам:')
        print('-' * 50)
        pprint(addressee)
        print('-' * 50)

        return addressee


# db_cash = TasksCash
# db_cash.generate_some_tasks()
# a = db_cash.get_mails()



