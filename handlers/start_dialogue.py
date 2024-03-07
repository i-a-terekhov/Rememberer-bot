from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InputFile, FSInputFile

from database import kvazi_db
from hidden.tokenfile import OWNER_CHAT_ID, TOKEN
from keyboards.inline import make_inline_rows_keyboard
from states.base import Entering


bot = Bot(TOKEN)

start_router = Router()


#TODO необходим хэндлер, для ловли любых сообщений (в том, числе /start) при статусе StateFilter(None),
# который будет проверять наличие юзера в БД (на случай перезагрузки бота или удаления юзером переписки).

@start_router.message(StateFilter(None))
async def recover_dialogue(message: Message):
    """
    Хэндлер, восстанавливающий состояние юзера (комнаты, роли) после перезагрузки бота
    """
    # сверяемся с базой: если нет юзера в бд - идем в стартовый диалог,
    # если юзер в бд: восстанавливаем его состояние из бд




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

    await callback.message.answer(
        text="Введите название комнаты (регистр имеет значение!)",
    )


@start_router.message(StateFilter(Entering.waiting_for_rooms_name))
async def check_rooms_name(message: Message, state: FSMContext) -> None:
    """
    Хэндлер проверки имени комнаты на предмет существования
    """

    print(f'Юзер {message.chat.id}: check_rooms_name')

    if message.text in kvazi_db.rooms_and_passwords.keys():
        print(f'Комната "{message.text}" существует, запрошен пароль')
        await state.set_state(Entering.waiting_for_new_rooms_password)
        await message.answer(text=f'Введите пароль для комнаты {message.text}')
    else:
        # В этом варианте стейт не меняется, но сохраняем введенное пользователем имя комнаты, на случай,
        # если пользователь захочет использовать это имя на следующем шаге
        await state.update_data(new_room_name=message.text)
        print(f'Комната не найдена, можно создать с введенным именем "{message.text}" или использовать другое имя')

        await message.answer(
            text="Комнаты с таким именем не существует! Вы можете ввести имя комнаты заново (просто напишите в чат).\n"
                 "Либо Вы можете создать комнату с введенным именем (кнопка).\n"
                 "Либо Вы можете создать комнату с другим именем (кнопка).",
            reply_markup=make_inline_rows_keyboard(['Использовать текущее имя', 'Выбрать другое имя'])
        )


@start_router.callback_query(F.data.in_(["Использовать текущее имя"]))
async def make_room_with_current_name(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Хэндлер обработки кнопки "Использовать текущее имя для комнаты",
    меняет состояние на "Ожидает ввод пароля для комнаты"
    """

    await callback.answer()
    print(f'Юзер {callback.from_user.id}: нажал на кнопку "Использовать текущее имя для комнаты"')

    user_data = await state.get_data()
    room_name = user_data.get("new_room_name")
    await callback.message.answer(
        text=f'Отлично! Теперь задайте пароль \nдля комнаты "{room_name}"!',
    )
    await state.set_state(Entering.waiting_for_new_rooms_password)


@start_router.message(StateFilter(Entering.waiting_for_new_rooms_password))
async def accept_the_password(message: Message, state: FSMContext) -> None:
    """
    Хэндлер ловит пароль новой для комнаты, имя которой передается в state, сохраняя получившуюся пару в kvazi_db
    """
    print(f'Юзер {message.chat.id}: accept_the_password')

    password = message.text
    user_data = await state.get_data()
    room_name = user_data.get("new_room_name")
    await message.answer(
        text=f'Для комнаты "{room_name}" был задан пароль: "{password}"!',
    )

    #TODO в дальнейшем для работы с БД будут созданы свои функции
    kvazi_db.rooms_and_passwords[room_name] = password
    print('Словарь комнат обновился:')
    print(kvazi_db.rooms_and_passwords)

    kvazi_db.users_and_roles[message.from_user.id] = {
        'nickname': message.from_user.username,
        'rooms': {room_name: 'admin'}
     }
    print('Словарь юзеров обновился:')
    print(kvazi_db.users_and_roles)

    await state.clear()

