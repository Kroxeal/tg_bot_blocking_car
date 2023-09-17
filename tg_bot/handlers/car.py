from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from tg_bot_aiogram.tg_bot.States.states import RegistrationCarStates
from tg_bot_aiogram.tg_bot.database.orm import Registration, session, UserManager

router = Router()


@router.message(Command('registration_car'))
async def start_registration_car(message: types.Message, state: FSMContext):
    await message.answer('Для регистрации машины введите, пожалуйста, марку автомобиля. ')
    await state.set_state(RegistrationCarStates.brand_car)


@router.message(RegistrationCarStates.brand_car)
async def enter_brand_car(message: types.Message, state: FSMContext):
    await state.update_data(brand_car=message.text)
    await message.answer('Введите год выпуска автомобиля. ')
    await state.set_state(RegistrationCarStates.model_car)


@router.message(RegistrationCarStates.model_car)
async def enter_model_car(message: types, state: FSMContext):
    await state.update_data(model_car=message.text)
    await message.answer('Введите год производства автомобиля. ')
    await state.set_state(RegistrationCarStates.year)


@router.message(RegistrationCarStates.year)
async def enter_year_car(message: types, state: FSMContext):
    await state.update_data(year=message.text)
    await message.answer('Введите регистрационный номер автомобиля в формате "3610 AM-1". ')
    await state.set_state(RegistrationCarStates.license_plate)


@router.message(RegistrationCarStates.license_plate)
async def enter_license_plate_car(message: types, state: FSMContext):
    await state.update_data(license_plate=message.text)
    await message.answer('Введите цвет автомобиля. ')
    await state.set_state(RegistrationCarStates.color)


@router.message(RegistrationCarStates.color)
async def enter_color_car(message: types, state: FSMContext):
    await state.update_data(color=message.text)
    data = await state.get_data()
    brand_car = data['brand_car']
    model_car = data['model_car']
    year = data['year']
    license_plate = data['license_plate']
    color = data['color']

    user_id = UserManager.get_user_id(message)

    Registration.add_car_to_user(
        user_id,
        brand_car,
        model_car,
        year,
        license_plate,
        color
    )

    await message.answer(
        f'Марка автомобиля: {brand_car}\n'
        f'Модель автомобиля: {model_car}\n'
        f'Год производства: {year}\n'
        f'Регистрационный знак: {license_plate}\n'
        f'Цвет: {color}\n'
    )

    await state.clear()
