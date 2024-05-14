import asyncio
from pprint import pprint

from aiogram import Bot

from keyboards.inline import make_inline_rows_keyboard, many_keys_in_row
from schedule.main_cash_objects import TasksCash
from schedule.time import current_datatime


async def send_message_with_bottoms(bot_unit: Bot, chat_id: str, text: str) -> None:
    """
    Функция отправки пользователю сообщения с кнопками готовности задачи
    """
    try:
        await bot_unit.get_chat(chat_id)
    except Exception as e:
        print(f"{current_datatime()}: Юзер '{chat_id}' не найден. Ошибка: {e} (send_message_for_check)")
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


# def _form_task_message_for_show(task: dict) -> str:
#     """
#     Функция формирования текстового сообщения из task для отправки юзеру
#     """
#     room_name = task['room']
#     task_text = task['text']
#     executor_id = task['executor']
#     create_time = task['create_time']
#     execution_level = task['execution_level']
#     accept_by_author = task['accept_by_author']
#
#     execut = int(execution_level * 100 // 10)
#     non_exec = 10 - execut
#     if accept_by_author:
#         accept = "V"
#     else:
#         accept = "X"
#     execution_bar = f'[{"#" * execut}{"-" * non_exec}][{accept}]'
#
#     text = f'{create_time}. Комната: {room_name}, ответственный {executor_id}.\n' \
#            f'Задача: {task_text}\n' \
#            f'Выполнение: {execution_bar}'
#     return text


async def going_through_all_tasks(bot_unit: Bot) -> None:
    """
    Функция достает из кэша БД задачу и передает в send_message_with_bottoms
    """
    db_cash = TasksCash()
    db_cash.generate_some_tasks()
    mails = db_cash.get_mails()
    print(f'{current_datatime()}: Обрабатываем задачи из буфера БД (going_through_all_tasks)')

    for room in mails:
        #TODO должен быть перебор telegram_id, а не символов, из которых состоит имя комнаты:
        for telegram_id in room:
            try:
                # TODO добавить отправку общего сообщения для пользователя
                text = f'Вы находитесь в комнате {room}, в которой для вас есть задачи:'
                await send_message_with_bottoms(bot_unit=bot_unit, chat_id=telegram_id, text=text)
            except TypeError:
                print(f'{current_datatime()}: Не удалось отправить задачу т.к. логин {telegram_id} не найден')


async def periodic_start_for_functions(bot: Bot) -> None:
    """
    Функция периодического запуска going_through_all_tasks
    """
    while True:
        await going_through_all_tasks(bot_unit=bot)
        await asyncio.sleep(60 * 2)
