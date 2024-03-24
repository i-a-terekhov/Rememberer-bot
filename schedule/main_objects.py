from pprint import pprint
from random import randint

from aiogram.types import Message

from schedule.time import current_datatime
from database import kvazi_db


class UserType:
    users = kvazi_db.users

    def __init__(self, message: Message):
        self.telegram_id = str(message.from_user.id)
        UserType.users.add(self.telegram_id)
        print('Множество в классе UserType: ', UserType.users)

    @classmethod
    def save_to_bd(cls):
        kvazi_db.users.update(cls.users)
        print(f'Квази-база после сохранения юзеров из класса:')
        pprint(kvazi_db.users)


class ConfigurateType:
    users_and_roles = kvazi_db.users_and_roles

    def __init__(self, room_name: str, message: Message, role: str):
        if role not in ['owner', 'admin', 'user']:
            raise ValueError("Role must be one of: 'owner', 'admin', 'user'")
        configurate = str(message.from_user.id) + '_in_' + room_name
        ConfigurateType.users_and_roles[configurate] = {
            'telegram_id': str(message.from_user.id),
            'nickname': message.from_user.username,
            'room': room_name,
            'role': role
        }

    @classmethod
    def save_to_bd(cls):
        kvazi_db.users_and_roles.update(cls.users_and_roles)
        print(f'Квази-база после сохранения конфигураций из класса:')
        pprint(kvazi_db.users_and_roles)


class RoomType:
    rooms_settings = kvazi_db.rooms_settings

    def __init__(self, room_name: str, message: Message):
        user_id = str(message.from_user.id)
        RoomType.rooms_settings[room_name] = {
            'name': room_name,
            'owner': user_id,
            'admins': [user_id],
            'members': [user_id],
            'password': message.text,
            'rights_to_create_task': 'all_users'
        }

    @classmethod
    def is_room_exist(cls, room_name: str):
        if room_name in cls.rooms_settings:
            return True
        else:
            return False

    @classmethod
    def is_password_correct(cls, room_name, password):
        if cls.rooms_settings[room_name]['password'] == password:
            return True
        else:
            return False

    @classmethod
    def save_to_bd(cls):
        kvazi_db.rooms_settings.update(cls.rooms_settings)
        print(f'Квази-база после сохранения комнат из класса:')
        pprint(kvazi_db.rooms_settings)


class Tasks:
    all_tasks = kvazi_db.all_tasks

    def __init__(self, room_name, text, author, executor):
        # self.number = "random number"  # уник. номер комнаты, будет генерится функцией
        self.new_task = {
                'room': room_name,
                'text': text,
                'author': author,
                'executor': executor,
                'create_time': current_datatime(),
                'period_of_remind': '30:00',
                'execution_level': 0.0,
                'accept_by_author': False,
                'accept_in_time': '2025-12-31 23:59',
                'livetime_after_ending': '12:00',
                'list_of_recipients': [author],
        }

    @classmethod
    def make_unic_number(cls) -> str:
        while True:
            number = str(randint(1, 1000))
            if number in cls.all_tasks.keys():
                continue
            else:
                return str(number)

    def save_task(self):
        number = Tasks.make_unic_number()
        Tasks.all_tasks[number] = self.new_task

    @classmethod
    def generate_tasks(cls):
        for i in range(1):
            room_name = kvazi_db.room_name
            text = f"Задача такая-то {randint(0, 10)}"
            author = kvazi_db.user_id
            executor = f"Исполнитель такой-то"
            task = Tasks(room_name, text, author, executor)
            task.new_task["execution_level"] = randint(0, 100) / 100
            Tasks.all_tasks['task_num_' + str(cls.make_unic_number())] = task.new_task
        return Tasks.all_tasks

    @classmethod
    def iter_tasks(cls):
        for task in cls.all_tasks:
            yield cls.all_tasks[task]


class AssignmentForMailing:
    all_tasks = kvazi_db.all_tasks
    addressee = {}
    # addressee = {'12213134': {
    #                 'room_id': ['task', 'task2', 'task3']
    #                   },
    #              '23452456': {
    #                  'room_id': ['task'],
    #                  'room2_id': ['task3', 'task2']
    #                 }
    #              }

    @classmethod
    def get_mails(cls):
        for rand_num, task in cls.all_tasks.items():
            executor = task['executor']
            room = task['room']
            # Если исполнитель уже есть в словаре addressee, добавляем комнату в его список
            if executor in cls.addressee:
                if room not in cls.addressee[executor]:
                    cls.addressee[executor][room] = [rand_num]
                else:
                    cls.addressee[executor][room].append(rand_num)
            # Если исполнителя нет в словаре addressee, добавляем его и его комнату
            else:
                cls.addressee[executor] = {room: [rand_num]}
        print('Вот:')
        pprint(cls.addressee)
        print('Вот')

        result = cls.addressee
        cls.addressee = {}
        return result



