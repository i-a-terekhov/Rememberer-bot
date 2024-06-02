import asyncio
from pprint import pprint

from aiogram import Bot

from keyboards.inline import make_inline_rows_keyboard, many_keys_in_row
from schedule.main_cash_objects import TasksCash, TimeToMail
from schedule.time import current_datatime


async def send_simple_message(bot_unit: Bot, chat_id: str, text: str) -> None:
    """
    Функция отправки пользователю сообщения с кнопками готовности задачи
    """
    await bot_unit.send_message(
        chat_id=chat_id,
        text=text,
    )


async def send_message_with_bottoms(bot_unit: Bot, chat_id: str, text: str) -> None:
    """
    Функция отправки пользователю сообщения с кнопками готовности задачи
    """
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


def _form_task_message_for_show(task: dict) -> str:
    """
    Функция формирования текстового сообщения из task для отправки юзеру
    """
    # room_name = task['room']
    task_text = task['text']
    executor_id = task['executor']
    create_time = task['create_time']
    execution_level = task['execution_level']
    accept_by_author = task['accept_by_author']

    execut = int(execution_level * 100 // 10)
    non_exec = 10 - execut
    if accept_by_author:
        accept = "V"
    else:
        accept = "X"
    execution_bar = f'[{"#" * execut}{"-" * non_exec}][{accept}]'

    text = f'{create_time}. {task_text}\n' \
           f'Ответственный {executor_id}.\n' \
           f'Выполнение: {execution_bar}\n'
    return text


async def sending_for_standard_mailings(bot_unit: Bot) -> None:
    """
    Функция отправляет пользователям сообщения с тасками, структурированные по принадлежности к комнатам.
    """
    db_cash = TasksCash()
    # db_cash.generate_some_tasks()  #TODO временная функция для наполнения кэша БД учебными данными
    mails = db_cash.get_mails()
    print(f'{current_datatime()}: Обрабатываем задачи из буфера БД (sending_all_standard_mailings)')

    unic_users_with_tasks = []
    for room in mails:
        for telegram_id in mails[room]:
            # print(f'Смотрим получателя {telegram_id}')
            try:
                await bot_unit.get_chat(telegram_id)
                if telegram_id not in unic_users_with_tasks:
                    unic_users_with_tasks.append(telegram_id)
            except Exception as e:
                # print(f"{current_datatime()}: Юзер '{telegram_id}' не найден. Ошибка: {e} (sending_all_standard_mailings)")
                continue
            final_text = f'В комнате {room}, есть задачи:\n'
            for task in mails[room][telegram_id]:
                final_text += '\n'
                final_text += _form_task_message_for_show(db_cash.all_tasks[task])

            await send_message_with_bottoms(bot_unit=bot_unit, chat_id=telegram_id, text=final_text)

    menu_text = 'Менюшка'
    for user in unic_users_with_tasks:
        await send_menu(bot_unit=bot_unit, chat_id=user, text=menu_text)


async def send_menu(bot_unit: Bot, chat_id: str, text: str) -> None:
    """
    Функция отправки сообщения с меню
    """
    await bot_unit.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=make_inline_rows_keyboard(['Мои комнаты', 'Мои задачи'])
    )


async def form_dict_for_mailings() -> dict:
    """
    Функция формирования словаря для отправки рассылок
    """
    print(f'{current_datatime()}: Формируем словарь для рассылок (form_dict_for_mailings)')
    time_to_mail = TimeToMail()
    users_list = time_to_mail.go_throw_timestamps()
    db_cash = TasksCash()
    mails = db_cash.get_mails(users_list)

    return mails


async def send_mailings(bot: Bot, mails: dict) -> None:
    pass


async def periodic_start_for_functions(bot: Bot) -> None:
    """
    Функция периодического запуска sending_all_standard_mailings
    """
    while True:
        mails = await form_dict_for_mailings()
        await send_mailings(bot=bot, mails=mails)
        await asyncio.sleep(15)
        # await asyncio.sleep(60 * 2)
