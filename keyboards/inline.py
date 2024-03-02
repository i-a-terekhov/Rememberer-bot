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


def make_inline_rows_keyboard(items: list[str]) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру с кнопками в несколько рядов по числу кнопок
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    rows = [[InlineKeyboardButton(text=str(item), callback_data=str(item))] for item in items]
    return InlineKeyboardMarkup(inline_keyboard=rows)
