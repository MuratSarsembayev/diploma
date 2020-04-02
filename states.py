from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    Send_City_A = State()
    Send_City_B = State()
    Send_Date = State()
    Take_City_A = State()
    Take_City_B = State()
    Take_Date = State()
