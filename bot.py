import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from hidden.tokenfile import TOKEN_FIVE as TOKEN
from hidden.tokenfile import OWNER_CHAT_ID as CHAT_ID

from handlers.echo_plug import service_router, regular_router
from classes.schedule import ListOfTasks


bot_unit = Bot(TOKEN)
tasks = ListOfTasks


# Для проверки работы periodic_start_for_functions
async def send_message_for_check():
    print('send_message_for_check')
    await bot_unit.send_message(chat_id=CHAT_ID, text="Привет, это ваше регулярное сообщение!")


async def send_message(text: str):
    print('send_message')
    await bot_unit.send_message(chat_id=CHAT_ID, text=text)


#TODO разобраться, что тут не так
async def check_list_of_tasks():
    if tasks.check_empty():
        text = 'Есть некоторые задачи'
    else:
        text = 'Нет задач'
    await send_message(text=text)


async def periodic_start_for_functions():
    print('periodic_start_for_functions')
    while True:
        await send_message_for_check()
        await asyncio.sleep(60 * 5)


async def main(bot: Bot):
    """
    Главная функция развертки поллинга диспетчера бота.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(
        storage=MemoryStorage(),
        maintenance_mode=True  # режим обслуживания бота (True - заглушка, False - более сложная заглушка)
    )

    dp.include_routers(
        service_router,
        regular_router,
        )

    await dp.start_polling(bot)


async def gathering_functions():
    await asyncio.gather(periodic_start_for_functions(), main(bot=bot_unit))


if __name__ == '__main__':
    asyncio.run(gathering_functions())





