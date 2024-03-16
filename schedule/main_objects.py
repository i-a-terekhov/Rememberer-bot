import asyncio
from pprint import pprint
from random import randint

from aiogram import Bot, exceptions
from aiogram.types import Message

from schedule.time import current_time
from database import kvazi_db


class UserType:
    users = kvazi_db.users

    def __init__(self, message: Message):
        self.telegram_id = str(message.from_user.id)
        UserType.users.add(self.telegram_id)
        print('Множество в классе UserType: ', UserType.users)

    @classmethod
    def save_to_bd(cls):
        # print(f'Квази-база до сохранения юзеров из класса:')
        # pprint(kvazi_db.users)
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
        # print(f'Квази-база до сохранения конфигураций из класса:')
        # pprint(kvazi_db.users_and_roles)
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
        # print(f'Квази-база до сохранения комнат из класса:')
        # pprint(kvazi_db.rooms_settings)
        kvazi_db.rooms_settings.update(cls.rooms_settings)
        print(f'Квази-база после сохранения комнат из класса:')
        pprint(kvazi_db.rooms_settings)



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


task_01 = Tasks(room_name='01', text='sadfas', author='me', executor='2342')


# Для проверки работы periodic_start_for_functions
async def send_message_for_check(bot_unit: Bot, chat_id: str, text: str):
    print(current_time(), ': send_message_for_check')
    # Получаем информацию о чате
    try:
        chat = await bot_unit.get_chat(chat_id)
    except Exception:
        print(f"Юзер '{chat_id}' не найден")
        return
    if not chat:
        print(f"Чат '{chat_id}' не существует")
        return

    await bot_unit.send_message(chat_id=chat_id, text=text)


async def check_list_of_tasks(bot_unit: Bot, chat_id: str):
    def check_empty():
        if len(Tasks.all_tasks) > 0:
            return True
        else:
            return False

    if check_empty():
        text = f'{current_time()}: Есть некоторые задачи'
    else:
        text = f'{current_time()}: Нет задач'
        task_01.save_task()
    await send_message_for_check(bot_unit=bot_unit, chat_id=chat_id, text=text)


async def check_is_user_in_rooms(bot_unit: Bot):
    for config in ConfigurateType.users_and_roles:
        chat_id = ConfigurateType.users_and_roles[config]["telegram_id"]
        text = f'Вы состоите в группе: {ConfigurateType.users_and_roles[config]["room"]}'
        await send_message_for_check(bot_unit=bot_unit, chat_id=chat_id, text=text)


async def periodic_start_for_functions(bot: Bot, chat_id: str):
    # Функция проходит по всему пулу задач, отправляя каждую в те чаты, которые указаны в каждой таске.
    # Если задач нет, ничего не происходит.
    # Задачи появляются по нажатию кнопки "создать задачу" и заполнении данных для нее.
    # Задачи исчезают по нажатию на одну из кнопок: "удалить задачу" или "задача выполнена" с рассылкой соответсвующего
    # сообщения всем участникам комнаты

    while True:
        await check_list_of_tasks(bot_unit=bot, chat_id=chat_id)
        await check_is_user_in_rooms(bot_unit=bot)
        await asyncio.sleep(60 * 2)

