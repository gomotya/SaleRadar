from bot_instance import bot
from app.database.requests import get_tg_ids_by_category
from app.database.models import Product
from sqlalchemy import select
from datetime import datetime
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.exceptions import TelegramForbiddenError
import logging


async def process_product(session, name, category, price, link, shop_name):
    # Используем асинхронный запрос для поиска продукта в базе
    existing_product = await session.execute(
        select(Product).where(Product.name == name, Product.shop_name == shop_name)
    )
    existing_product = existing_product.scalar()

    if existing_product:
        # Если продукт найден, проверяем цену
        if existing_product.price > price:
            message_text = (
                f"КАТЕГОРИЯ '{category}' \n"
                f"Цена товара '{name}' уменьшилась.\n"
                f"Старая цена: {existing_product.price} ₽\n"
                f"Новая цена: {price} ₽\n"
            )
            await notify_users(message_text, category, link)

        # Обновляем цену, если она изменилась
        if existing_product.price != price:
            existing_product.price = price
            existing_product.date = datetime.now().date()
            await session.commit()  # Сохраняем изменения
    else:
        # Если продукт не найден, создаем новый
        new_product = Product(
            name=name,
            category=category,
            price=price,
            link=link,
            date=datetime.now().date(),
            shop_name=shop_name
        )
        session.add(new_product)
        await session.commit()  # Сохраняем новый продукт


async def notify_users(text_message, category, link):
    tg_ids = await get_tg_ids_by_category(category)
    if not tg_ids:
        print(f"Нет подписчиков для категории: {category}")
        return
    
    button = InlineKeyboardButton(text="Ссылка 🔥", url=link)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])  
    for tg_id in tg_ids:  
        try:
            await bot.send_message(tg_id, text_message, reply_markup=keyboard)
        except TelegramForbiddenError:
            # Логируем ошибку и продолжаем выполнение
            print(f"Пользователь {tg_id} заблокировал бота. Сообщение не отправлено.")
            await bot.send_message(
                    553450853, 
                    f"Пользователь {tg_id} заблокировал бота. Сообщение не отправлено."
            )
            logging.warning(f"Пользователь {tg_id} заблокировал бота. Сообщение не отправлено.")
        
        