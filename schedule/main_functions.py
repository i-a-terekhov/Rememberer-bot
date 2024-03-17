import asyncio
from pprint import pprint

from aiogram import Bot

from schedule.main_objects import Tasks, ConfigurateType
from schedule.time import current_time

# Для проверки работы periodic_start_for_functions
example_tasks = Tasks.generate_tasks()

#TODO первый шаг: итерируемся по конфигурациям, вытаскивая ID_юзера, группу и досупные юзеру задачи


async def send_message_for_check(bot_unit: Bot, chat_id: str, text: str):
    print(current_time(), ': send_message_for_check')
    try:
        await bot_unit.get_chat(chat_id)
    except Exception:
        print(f"Юзер '{chat_id}' не найден")
        return
    await bot_unit.send_message(chat_id=chat_id, text=text)


async def check_list_of_tasks(bot_unit: Bot, chat_id: str):
    if len(Tasks.all_tasks) > 0:
        text = f'{current_time()}: Есть некоторые задачи ({len(Tasks.all_tasks)})'
        pprint(Tasks.all_tasks)
    else:
        text = f'{current_time()}: Нет задач'
        example_tasks.save_task()
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
