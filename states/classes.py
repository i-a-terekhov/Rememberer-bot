from aiogram.fsm.state import StatesGroup, State


class Entering(StatesGroup):
    waiting_for_rooms_name = State()

