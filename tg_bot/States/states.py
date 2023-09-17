from aiogram.fsm.state import StatesGroup, State


class RegistrationUserStates(StatesGroup):
    first_name = State()
    last_name = State()
    phone_number = State()


class RegistrationCarStates(StatesGroup):
    brand_car = State()
    model_car = State()
    year = State()
    license_plate = State()
    color = State()


class IsBlocked(StatesGroup):
    license_plate = State()
    answer = State()
    chat_id = State()


class MyCarBlockes(IsBlocked):
    license_plate = State()
    answer = State()
    chat_id = State()

