from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from tg_bot_aiogram.tg_bot.States.states import IsBlocked
from tg_bot_aiogram.tg_bot.app import bot
from tg_bot_aiogram.tg_bot.database.orm import CarManager
from tg_bot_aiogram.tg_bot.keyboards import kb_is_blocked

router = Router()


@router.message(Command('is_blocked'))
async def is_blocked(message: types.Message, state: FSMContext):
    await message.answer('Введите регистрационный номер машины, которая вас подперла. ')
    await state.set_state(IsBlocked.license_plate)


@router.message(IsBlocked.license_plate)
async def enter_license_plate(message: types.Message, state: FSMContext):
    await state.update_data(license_plate=message.text)
    data = await state.get_data()
    license_plate = data['license_plate']
    owners = CarManager.get_users_by_license_plate(license_plate=license_plate)
    if owners:
        for owner in owners:
            await message.answer(
                f'Владелец данного автомобиля @{owner.username}\n'
                f'Имя: {owner.first_name}\n'
                f'Номер телефона: {owner.phone_number}\n'
            )
            await state.update_data(chat_id=owner.id)
        await message.answer('Сообщить владельцу о том, что он вас подпер?! ', reply_markup=kb_is_blocked.keyboard_is_blocked)
        await state.set_state(IsBlocked.answer)
    else:
        await message.answer('К сожалению, владельцев данного автомобиля не найдено :( ')


@router.message(IsBlocked.answer)
async def enter_answer(message: types.Message, state: FSMContext):
    await state.update_data(answer=message.text)
    data = await state.get_data()
    if str(data['answer']) == 'Да':
        await message.answer('Отличный выбор!)', reply_markup=ReplyKeyboardRemove())
        username = message.from_user.username
        await writing_message(username=username, state=state)
        await state.clear()
    else:
        await message.answer(f'Ну ладно :( ')
        await state.clear()


async def writing_message(username, state: FSMContext):
    data = await state.get_data()
    chat_id = data['chat_id']
    car_info = CarManager.get_car_info(username=username)

    if car_info:
        for brand_car, license_plate in car_info:
            text = \
                f"Вы подперли автомобиль марки: {brand_car}, \n"\
                f"Регистрационный номер: {license_plate}, \n"\
                f"Просим убрать автомобиль!"
            await bot.send_message(chat_id=chat_id, text=text)
