from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from tg_bot_aiogram.tg_bot.States.states import RegistrationUserStates
from tg_bot_aiogram.tg_bot.database.orm import Registration, session, UserManager

router = Router()


@router.message(Command('registration_user'))
async def start_registration_user(message: types.Message, state: FSMContext):
    username = message.from_user.username if message.from_user.username else None
    if UserManager.is_username_exists(username, session):
        await message.answer('Вы уже зарегистрированы!')
        return
    await message.answer('Для регистрации введите, пожалуйста, ваше имя.')
    await state.set_state(RegistrationUserStates.first_name)


@router.message(RegistrationUserStates.first_name)
async def enter_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer('Введите фамилию. ')
    await state.set_state(RegistrationUserStates.last_name)


@router.message(RegistrationUserStates.last_name)
async def enter_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer('Введите номер телефона в формате +375443579518 ')
    await state.set_state(RegistrationUserStates.phone_number)


@router.message(RegistrationUserStates.phone_number)
async def enter_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    data = await state.get_data()
    first_name = data['first_name']
    last_name = data['last_name']
    phone_number = data['phone_number']

    Registration.registration_user(message, first_name, last_name, phone_number)

    await message.answer(
        f'Имя: {first_name}\n'
        f'Фамилия: {last_name}\n'
        f'Номер телефона: {phone_number}\n'
    )

    await state.clear()
