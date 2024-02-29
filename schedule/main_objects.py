import asyncio

from aiogram import Bot


class RegularSchedule:
    def __init__(self):
        pass


#TODO Сделать описание
class ListOfTasks:
    def __init__(self):
        self.list_of_tasks = list()

    def check_empty(self):
        if len(self.list_of_tasks) == 0:
            return False
        else:
            return True

    def add_task(self, describe: str):
        self.list_of_tasks.append(describe)


#TODO Сделать описание
class Task:
    def __init__(self, room, text, category, reminder_time):
        self.room = room  # уник. имя комнаты - ключ в словаре, значения для которого - лист с ID участников комнаты
        self.text = text  # текст задачи - нулевое значение листа, остальные значения листа - подзадачи
        self.reminder_time = reminder_time

    def __str__(self):
        return f"Task: {self.text}, Text: {self.text}, Reminder Time: {self.reminder_time}"

    def make_task(self):
        default_list_of_tasks = [
            'Не забыть сделать',
            'Не забыть купить',
            'Не забыть посетить',
            'Обновить пароли на сервисы'
        ]


#TODO Сделать описание
# Класс Room создает экземпляры комнат, основной задачей которых является сохранение списка участников, для рассылки им
# сообщений с задачами и сообщений о поставленных и выполненных задачах
# Функционал комнат должен подразумевать наличие роли админа (одного или нескольких).
# Админ решает, кто может добавлять задачи (только админы или все), кто может утвердить задачу
# выполненной (только админы или все), производится ли рассылка задач всем или только ответственным.

class Room:
    def __init__(self, room_name):
        self.room_name = room_name
        self.members = []
        self.categories = []
        self.tasks = []

    def add_member(self, user_id):
        self.members.append(user_id)

    def create_task(self, text, category, reminder_time):
        task = Task(text, category, reminder_time)
        self.tasks.append(task)
        return task


tasks = ListOfTasks()


# Для проверки работы periodic_start_for_functions
async def send_message_for_check(bot_unit: Bot, chat_id: str, text: str):
    print('send_message_for_check')
    await bot_unit.send_message(chat_id=chat_id, text=text)


async def check_list_of_tasks(bot_unit: Bot, chat_id: str):
    if tasks.check_empty():
        text = 'Есть некоторые задачи'
    else:
        text = 'Нет задач'
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

