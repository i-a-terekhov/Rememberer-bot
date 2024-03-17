import asyncio
from pprint import pprint

from aiogram import Bot

from keyboards.inline import make_inline_rows_keyboard, many_keys_in_row
from schedule.main_objects import Tasks, ConfigurateType
from schedule.time import current_time

# Для проверки работы periodic_start_for_functions
example_tasks = Tasks.generate_tasks()

#TODO первый шаг: итерируемся по конфигурациям, вытаскивая ID_юзера, группу и досупные юзеру задачи
#TODO формируем сообщение из доступных юзеру задач


async def send_message_for_check(bot_unit: Bot, chat_id: str, text: str):
    try:
        await bot_unit.get_chat(chat_id)
    except Exception:
        print(f"Юзер '{chat_id}' не найден")
        return
    await bot_unit.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=many_keys_in_row([
            ('+1/4', 'callback_data_01'),
            ('+1/3', 'callback_data_02'),
            ('+1/2', 'callback_data_03'),
            ('Всё!', 'callback_data_04')]
             )
    )


async def going_through_all_tasks(bot_unit: Bot):
    for task in Tasks.iter_tasks():
        text = task["text"]
        room = task["room"]
        execution_level = task["execution_level"]
        chat_id = task["author"]
        print(f'Смотрим на задачу {text} из комнаты {room}')
        text += f' (выполнено: {execution_level})'
        await send_message_for_check(bot_unit=bot_unit, chat_id=chat_id, text=text)


# TODO удалить: временная функция для проверки класса Tasks
async def check_list_of_tasks(bot_unit: Bot, chat_id: str):
    if len(Tasks.all_tasks) > 0:
        text = f'{current_time()}: Есть некоторые задачи ({len(Tasks.all_tasks)}), но добавим еще...'
        Tasks.generate_tasks()
        pprint(Tasks.all_tasks)
    else:
        text = f'{current_time()}: Нет задач'
        example_tasks.save_task()
    await send_message_for_check(bot_unit=bot_unit, chat_id=chat_id, text=text)


# TODO удалить: временная функция для проверки класса ConfigurateType
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
        # await check_list_of_tasks(bot_unit=bot, chat_id=chat_id)
        # await check_is_user_in_rooms(bot_unit=bot)
        await going_through_all_tasks(bot_unit=bot)
        await asyncio.sleep(60 * 2)
