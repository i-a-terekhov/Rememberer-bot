from aiogram.fsm.state import StatesGroup, State


class Entering(StatesGroup):
    waiting_for_new_rooms_name = State()
    waiting_for_old_rooms_name = State()
    waiting_for_new_rooms_password = State()
    waiting_for_old_rooms_password = State()


