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
