import os
from aiogram import Bot
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла

load_dotenv()

API = os.getenv('TOKEN')
# Получаем токен

if not API:
    raise ValueError("Токен бота не найден.")

# Создаем экземпляр бота
bot = Bot(token=API)
