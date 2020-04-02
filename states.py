from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    Send_City_A = State()
    Send_City_B = State()
    Send_Day = State()
    Send_Month = State()
    Send_Year = State()
    Take_City_A = State()
    Take_City_B = State()
    Take_Day = State()
    Take_Month = State()
    Take_Year = State()