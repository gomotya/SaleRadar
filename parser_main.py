import asyncio
from parser_manager import run_parsers
from app.database.models import async_session
from app.database.requests import update_random_product_price

async def db_connect():
    async with async_session() as session:
        return session

# Главная функция для работы с парсерами
async def main():
    try:
        while True:
            # Получаем сессию
            async with async_session() as session:
                await run_parsers(session)  # Передаем связь с БД в функцию парсинга / запускаем парсинги
            await asyncio.sleep(60)  # Задержка 10 минут (600 секунд)
            await update_random_product_price()
    finally:
        # Закрытие сессии происходит автоматически
        pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Parser off')