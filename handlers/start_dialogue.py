from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from random import choice

from hidden.tokenfile import TOKEN
from keyboards.inline import make_inline_rows_keyboard
from states.base import Entering


bot = Bot(TOKEN)

start_router = Router()


@start_router.message(Command("start"), StateFilter(None))
async def start_dialogue(message: Message):
    """
    Старовый диалог.
    Хэндлер проверяет наличие юзера в БД и либо предлагает зарегистрироваться, либо выдает стандартные кнопки.

    """

    # user = UserType(message=message)
    # user.save_to_bd()
    user = choice([0, 1])

    await message.answer(reply_markup=ReplyKeyboardRemove(), text='Добрый день!')
    if user:
        await message.answer(
            text="Я Вас узнал! Продолжим работу!",
            reply_markup=make_inline_rows_keyboard(['Войти в комнату', 'Создать комнату'])
        )
        # + функция выдачи актуальных задач
    else:
        await message.answer(
            text="Я бот-ассистент для задач, которым не нашлось места в расписании!\n"
                 "Вы сможете оставлять задачи в чате, а я будут периодически о них напоминать\n"
                 "Более того, вы сможете создать одну или несколько комнат и пригласить туда других людей,"
                 "чтобы координировать выполнение задач или отслеживать их выполнение.",
            reply_markup=make_inline_rows_keyboard(['Начнем работу!'])
        )


# Фильтр "StateFilter(None)" для того, чтобы после однократного нажатия, кнопка перестала реагировать:
@start_router.callback_query(F.data.in_(["Войти в комнату"]), StateFilter(None))
@start_router.callback_query(F.data.in_(["Выбрать другую комнату"]), StateFilter(Entering.waiting_for_old_rooms_password))
async def ask_for_rooms_name(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Хэндлер обработки кнопки "Войти в комнату" или кнопки "Выбрать другую комнату" после неудачной попытки ввода пароля.
    Меняет состояние на "Ожидает имя существующей комнаты"
    """
    await callback.answer()

    await state.set_state(Entering.waiting_for_exist_room_name)
    await callback.message.answer(
        text="Введите название комнаты (регистр имеет значение!)",
    )


# @start_router.message(StateFilter(Entering.waiting_for_old_rooms_name))
# async def check_old_room_name(message: Message, state: FSMContext) -> None:
#     """
#     Хэндлер проверки имени комнаты на предмет существования
#     """
#     room_name = message.text
#     await state.update_data(current_room_name=room_name)
#
#     if RoomType.is_room_exist(room_name=room_name):
#         await state.set_state(Entering.waiting_for_old_rooms_password)
#         await message.answer(text=f'Введите пароль для комнаты {message.text}')
#     else:
#         await message.answer(
#             text="Комнаты с таким именем не существует! Вы можете ввести имя комнаты заново (просто напишите в чат).\n"
#                  "Либо Вы можете создать комнату с введенным именем (кнопка).\n",
#             reply_markup=make_inline_rows_keyboard(['Использовать текущее имя'])
#         )


# @start_router.message(StateFilter(Entering.waiting_for_old_rooms_password))
# async def check_old_room_password(message: Message, state: FSMContext) -> None:
#     """
#     Хэендлер для проверки пароля существующей комнаты
#     """
#     password = message.text
#     user_data = await state.get_data()
#     room_name = user_data.get("current_room_name")
#
#     if RoomType.is_password_correct(room_name=room_name, password=password):
#         config = ConfigurateType(room_name=room_name, message=message, role='user')
#         await message.answer(text=f'Отлично! Вы вошли в комнату: {room_name}')
#         config.save_to_bd()
#         await state.clear()
#     else:
#         await message.answer(
#             text=f'Неверный пароль! Попробуйте еще раз.',
#             reply_markup=make_inline_rows_keyboard(['Выбрать другую комнату']
#                                                    )
#         )


@start_router.callback_query(F.data.in_(["Использовать текущее имя"]), StateFilter(Entering.waiting_for_exist_room_name))
async def make_room_with_current_name(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Хэндлер обработки кнопки "Использовать текущее имя для комнаты",
    меняет состояние на "Ожидает ввод пароля для новой комнаты"
    """
    await callback.answer()

    user_data = await state.get_data()
    room_name = user_data.get("current_room_name")
    await callback.message.answer(
        text=f'Отлично! Теперь задайте пароль \nдля комнаты "{room_name}"!',
    )
    await state.set_state(Entering.waiting_for_new_rooms_password)


# @start_router.message(StateFilter(Entering.waiting_for_new_rooms_password))
# async def save_password_for_new_room(message: Message, state: FSMContext) -> None:
#     """
#     Хэндлер ловит пароль новой для комнаты, имя которой передается в state, сохраняя получившуюся пару в kvazi_db
#     """
#     password = message.text
#     user_data = await state.get_data()
#     room_name = user_data.get("current_room_name")
#
#     config = ConfigurateType(room_name=room_name, message=message, role='owner')
#     config.save_to_bd()
#
#     room = RoomType(room_name=room_name, message=message)
#     room.save_to_bd()
#
#     await message.answer(
#         text=f'Для комнаты "{room_name}" был задан пароль: "{password}"!',
#     )
#     await state.clear()


@start_router.callback_query(F.data.in_(["Создать комнату"]), StateFilter(None))
async def ask_for_new_rooms_name(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Хэндлер обработки кнопки "Создать комнату", меняет состояние на "Ожидает имя новой комнаты"
    """
    await callback.answer()

    await state.set_state(Entering.waiting_for_new_rooms_name)
    await callback.message.answer(
        text="Введите название комнаты (регистр имеет значение!)",
    )


# @start_router.message(StateFilter(Entering.waiting_for_new_rooms_name))
# async def check_new_room_name(message: Message, state: FSMContext) -> None:
#     """
#     Хэндлер проверки имени комнаты на предмет существования
#     """
#     if RoomType.is_room_exist(room_name=message.text):
#         await message.answer(
#             text="Комната с таким именем уже существует! Вы можете ввести имя комнаты заново (просто напишите в чат)."
#         )
#     else:
#         await state.update_data(current_room_name=message.text)
#         await state.set_state(Entering.waiting_for_new_rooms_password)
#         await message.answer(text=f'Введите пароль для комнаты {message.text} (просто напишите в чат).')
