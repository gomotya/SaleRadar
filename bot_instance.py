import os
from aiogram import Bot
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла

load_dotenv()
# Получаем токен
token = os.getenv('TOKEN')
if not token:
    raise ValueError("Токен бота не найден. Проверьте, что он задан в .env файле")

# Создаем экземпляр бота
bot = Bot(token=token)
