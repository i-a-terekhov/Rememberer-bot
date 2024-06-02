from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def one_key(text: str, callback_data: str) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру с одной кнопкой
    :param text: текст кнопки
    :param callback_data: текст каллбека
    :return: объект реплай-клавиатуры
    """
    row = [InlineKeyboardButton(text=text, callback_data=callback_data)]
    return InlineKeyboardMarkup(inline_keyboard=[row])


def many_keys_in_row(buttons: list[tuple]) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру с одной или несколькими кнопками
    :param buttons: список кортежей вида (текст кнопки, текст каллбека)
    :return: объект реплай-клавиатуры
    """
    keyboard_buttons = []
    for text, callback_data in buttons:
        keyboard_buttons.append(InlineKeyboardButton(text=text, callback_data=callback_data))
    return InlineKeyboardMarkup(inline_keyboard=[keyboard_buttons])


def many_keys_in_many_rows(buttons: list[list[tuple]]) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру с одной или несколькими кнопками в один или несколько рядов
    :param buttons: список списков с кортежами вида (текст кнопки, текст каллбека)
    :return: объект реплай-клавиатуры
    """
    keyboard = []
    for row in buttons:
        keyboard_row = []
        # keyboard_buttons = []
        for text, callback_data in row:
            # keyboard_buttons.append(InlineKeyboardButton(text=text, callback_data=callback_data))
            keyboard_row.append(InlineKeyboardButton(text=text, callback_data=callback_data))
        keyboard.append(keyboard_row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def make_inline_rows_keyboard(items: list[str]) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру с кнопками в несколько рядов по числу кнопок
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    rows = [[InlineKeyboardButton(text=str(item), callback_data=str(item))] for item in items]
    return InlineKeyboardMarkup(inline_keyboard=rows)
