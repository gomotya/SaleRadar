import asyncio
from aiogram import Dispatcher

from app.handlers import router
from app.database.models import async_main
from bot_instance import bot 

async def main():
    await async_main()

    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot off')