from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InputFile, FSInputFile

from database import kvazi_db
from hidden.tokenfile import OWNER_CHAT_ID, TOKEN
from keyboards.inline import make_inline_rows_keyboard
from states.classes import Entering


bot = Bot(TOKEN)

start_router = Router()


@start_router.message(Command("start"), StateFilter(None))
async def start_dialogue(message: Message):
    """
    Старовый диалог для создания комнаты или входа в имеющуюся
    """

    print(f'Юзер {message.chat.id}: start_dialogue')
    await message.answer(reply_markup=ReplyKeyboardRemove(), text='Добрый день!')

    await message.answer(
        text="Я бот-ассистент для задач, которым не нашлось места в расписании!\n"
             "Вы можете войти в имеющуюся комнату (если знаете название комнаты и пароль) или создать новую "
             "(можно находится в нескольких комнатах одновременно)!\n",
        reply_markup=make_inline_rows_keyboard(['Войти в комнату', 'Создать комнату'])
    )


# Фильтр "StateFilter(None)" для того, чтобы после однократного нажатия, кнопка перестала реагировать:
@start_router.callback_query(F.data.in_(["Войти в комнату"]), StateFilter(None))
async def ask_for_rooms_name(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Хэндлер обработки кнопки "Войти в комнату", меняет состояние на "Ожидает имя комнаты"
    """

    await callback.answer()
    print(f'Юзер {callback.from_user.id}: нажал на кнопку "Войти в комнату"')

    # Задаем стейт ожидания имени комнаты
    await state.set_state(Entering.waiting_for_rooms_name)
    #TODO при стейте waiting_for_rooms_name и вводе несуществующей комнаты, необходимо выводить
    # кнопки "попробовать еще", "создать комнату с этим именем", "создать комнату с другим именем"

    await callback.message.answer(
        text="Введите название комнаты (регистр имеет значение!)",
    )


@start_router.message(StateFilter(Entering.waiting_for_rooms_name))
async def check_rooms_name(message: Message, state: FSMContext) -> None:
    """
    Хэндлер проверки имени комнаты на предмет существования
    """

    print(f'Юзер {message.chat.id}: check_rooms_name')

    if message.text in kvazi_db.rooms_name:
        print('Комната существует, надо запросить пароль')
    else:
        print(f'Комната не найдена, можно создать с введенным именем "{message.text}" или использовать другое имя')
