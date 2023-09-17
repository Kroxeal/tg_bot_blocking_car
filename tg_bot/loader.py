import os

from aiogram import Bot, Dispatcher

from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=str(os.environ.get('TOKEN')), parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
