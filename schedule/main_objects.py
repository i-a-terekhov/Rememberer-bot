import asyncio
from random import randint

from aiogram import Bot
from aiogram.types import Message

from schedule.time import current_time


class RegularSchedule:
    def __init__(self):
        pass


class Users:
    users = tuple()

    def __init__(self, message: Message):
        self.telegram_id = message.from_user.id
        self.nickname = message.from_user.username
        Users.users = (self.telegram_id, )
        print('Словарь юзеров: ', Users.users)


class Rooms:
    users_and_roles = {}

    def __init__(self, room_name: str, message: Message):
        user_id = str(message.from_user.id)

        self.name = room_name
        self.owner = user_id
        self.admins = [user_id]
        self.members = [user_id]
        self.password = message.text
        self.rights_to_create_task = 'all_users'

        configurate = user_id + '_&_' + room_name
        Rooms.users_and_roles[configurate] = {
                'telegram_id': user_id,
                'nickname': message.from_user.username,
                'room': room_name,
                'role': 'admin'
            }

    @classmethod
    def is_room_exist(cls, room_name: str):
        if room_name in cls.users_and_roles:
            return True
        else:
            return False

    def add_user_to_room(self, room_name: str, message: Message):
        configurate = str(message.from_user.id) + '_&_' + room_name
        Rooms.users_and_roles[configurate] = {
            'telegram_id': str(message.from_user.id),
            'nickname': message.from_user.username,
            'room': room_name,
            'role': 'user'
        }


class Tasks:
    all_tasks = {}

    def __init__(self, room_name, text, author, executor):
        # self.number = "random number"  # уник. номер комнаты, будет генерится функцией
        self.new_task = {
                'room': room_name,
                'text': text,
                'author': author,
                'executor': executor,
                'period_of_remind': '30:00',
                'execution_level': 0.0,
                'accept_by_author': False,
                'accept_in_time': '2025-12-31 23:59:59',
                'livetime_after_ending': '12:00:00',
                'list_of_recipients': [author],
        }

    @classmethod
    def _is_task_number_exist(cls, number: str):
        if number in cls.all_tasks.keys():
            return True
        else:
            return False

    def _make_unice_number(self) -> str:
        while True:
            number = str(randint(1, 1000))
            if Tasks._is_task_number_exist(number):
                continue
            else:
                return str(number)

    def save_task(self):
        number = Tasks._make_unice_number(self)
        Tasks.all_tasks[number] = self.new_task


def check_empty():
    if len(Tasks.all_tasks) > 0:
        return True
    else:
        return False


task_01 = Tasks(room_name='01', text='sadfas', author='me', executor='2342')


# Для проверки работы periodic_start_for_functions
async def send_message_for_check(bot_unit: Bot, chat_id: str, text: str):
    print(current_time(), ': send_message_for_check')
    await bot_unit.send_message(chat_id=chat_id, text=text)


async def check_list_of_tasks(bot_unit: Bot, chat_id: str):

    if check_empty():
        text = f'{current_time()}: Есть некоторые задачи'
    else:
        text = f'{current_time()}: Нет задач'
        task_01.save_task()
    await send_message_for_check(bot_unit=bot_unit, chat_id=chat_id, text=text)


async def periodic_start_for_functions(bot: Bot, chat_id: str):
    # Функция проходит по всему пулу задач, отправляя каждую в те чаты, которые указаны в каждой таске.
    # Если задач нет, ничего не происходит.
    # Задачи появляются по нажатию кнопки "создать задачу" и заполнении данных для нее.
    # Задачи исчезают по нажатию на одну из кнопок: "удалить задачу" или "задача выполнена" с рассылкой соответсвующего
    # сообщения всем участникам комнаты

    while True:
        await check_list_of_tasks(bot_unit=bot, chat_id=chat_id)
        await asyncio.sleep(60 * 2)

