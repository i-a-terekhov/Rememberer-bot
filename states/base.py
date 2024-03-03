from aiogram.fsm.state import StatesGroup, State


class Entering(StatesGroup):
    waiting_for_rooms_name = State()
    #TODO понять, нужно ли два состояния для ожидания задания пароля и ожидания ввода имеющегося пароля
    waiting_for_rooms_password = State()

