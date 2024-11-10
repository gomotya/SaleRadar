from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
InlineKeyboardButton, InlineKeyboardMarkup)

from app.database.requests import get_categories

from aiogram.utils.keyboard import InlineKeyboardBuilder                           

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Категории')],
                                     [KeyboardButton(text='О нас')]],
                            resize_keyboard=True,
                            input_field_placeholder='Выберете пункт меню')

async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    keyboard.add(InlineKeyboardButton(text='Мои категории', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()

async def delete_user_category(category):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Удалить подписку', callback_data=f'delete_user_category_{category}'))
    return keyboard.adjust(1).as_markup()

my_category = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Мои категории')],
                                     [KeyboardButton(text='О нас')]],
                            resize_keyboard=True,
                            input_field_placeholder='Выберете пункт меню')