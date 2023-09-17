from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from tg_bot_aiogram.tg_bot.States.states import MyCarBlockes
from tg_bot_aiogram.tg_bot.app import bot
from tg_bot_aiogram.tg_bot.database.orm import CarManager
from tg_bot_aiogram.tg_bot.keyboards import kb_main_menu

router = Router()

'''
В разработке)
'''


@router.message(Command('main_menu', 'start'))
async def is_blocked(message: types.Message, state: FSMContext):
    await message.answer('Выберите действие: ', reply_markup=kb_main_menu.keyboard_menu)
    await state.set_state(MyCarBlockes.license_plate)
