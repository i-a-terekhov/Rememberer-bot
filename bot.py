import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from hidden.tokenfile import TOKEN_FIVE as TOKEN
from hidden.tokenfile import OWNER_CHAT_ID as CHAT_ID

from handlers.echo_plug import service_router, regular_router
from handlers.start_dialogue import start_router
from schedule.main_objects import periodic_start_for_functions


bot_unit = Bot(TOKEN)


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
        start_router,
        # service_router,
        # regular_router,
        )

    await dp.start_polling(bot)


async def gathering_functions():
    await asyncio.gather(
        periodic_start_for_functions(bot=bot_unit, chat_id=CHAT_ID),
        main(bot=bot_unit)
    )


if __name__ == '__main__':
    asyncio.run(gathering_functions())





