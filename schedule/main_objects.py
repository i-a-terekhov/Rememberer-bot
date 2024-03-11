import asyncio

from aiogram import Bot
from aiogram.types import Message

from schedule.time import current_time


class RegularSchedule:
    def __init__(self):
        pass


class Users:
    def __init__(self, message: Message):
        self.telegram_id = message.from_user.id
        self.nickname = message.from_user.username


class Room:
    users_and_roles = {}

    def __init__(self, room_name, message: Message):
        self.name = room_name
        self.owner = message.from_user.id
        self.admins = [message.from_user.id]
        self.members = [message.from_user.id]
        self.password = message.text
        self.rights_to_create_task = 'all_users'

    def add_configurate(self, user_id, room_name):
        configurate = 'user_id' + '_&_' + 'room_name'
        self.users_and_roles[configurate] = {
                'telegram_id': user_id,
                'nickname': self.owner,
                'room': room_name,
                'role': 'admin'
            }


class Task:
    def __init__(self, room_name, text, author, executor):
        self.number = "random number"  # уник. номер комнаты, будет генерится функцией
        self.room = room_name
        self.text = text  # текст задачи
        self.author = author
        self.executor = executor
        self.period_of_remind = '30:00'
        self.execution_level = 0.0
        self.accept_by_author = False
        self.accept_in_time = '2025-12-31 23:59:59'
        self.livetime_after_ending = '12:00:00'
        self.list_of_recipients = [author]

    def __str__(self):
        return f"Task: {self.text}, Text: {self.text}, Accept in Time: {self.accept_in_time}"


# Класс ListOfTasks создает экземпляр хранилища всех задач, не различая задачи между комнатами
class ListOfTasks:
    def __init__(self):
        self.list_of_tasks = list()

    def check_empty(self):
        if len(self.list_of_tasks) == 0:
            return False
        else:
            return True

    def add_task(self, describe: Task):
        self.list_of_tasks.append(describe)


tasks = ListOfTasks()


# Для проверки работы periodic_start_for_functions
async def send_message_for_check(bot_unit: Bot, chat_id: str, text: str):
    print(current_time(), ': send_message_for_check')
    await bot_unit.send_message(chat_id=chat_id, text=text)


async def check_list_of_tasks(bot_unit: Bot, chat_id: str):
    if tasks.check_empty():
        text = f'{current_time()}: Есть некоторые задачи'
    else:
        text = f'{current_time()}: Нет задач'
        tasks.add_task('Первая задача!')
    await send_message_for_check(bot_unit=bot_unit, chat_id=chat_id, text=text)


async def periodic_start_for_functions(bot: Bot, chat_id: str):
    # Функция проходит по всему пулу задач, отправляя каждую в те чаты, которые указаны в каждой таске.
    # Если задач нет, ничего не происходит.
    # Задачи появляются по нажатию кнопки "создать задачу" и заполнении данных для нее.
    # Задачи исчезают по нажатию на одну из кнопок: "удалить задачу" или "задача выполнена" с рассылкой соответсвующего
    # сообщения всем участникам комнаты

    while True:
        await check_list_of_tasks(bot_unit=bot, chat_id=chat_id)
        await asyncio.sleep(60 * 5)

