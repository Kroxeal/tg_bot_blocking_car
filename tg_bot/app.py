import asyncio
import os
from dotenv import find_dotenv, load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

bot = Bot(token=str(os.environ.get('BOT_TOKEN')))
dp = Dispatcher(storage=MemoryStorage())


async def main():
    from tg_bot_aiogram.tg_bot.handlers import car, user, is_blocked, my_car_blockes

    dp.include_routers(
        user.router,
        car.router,
        is_blocked.router,
        my_car_blockes.router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
