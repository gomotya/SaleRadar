from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import app.keyboards as kb
import app.database.requests as rq
from app.database.requests import get_category_by_id


router = Router()


@router.message(CommandStart())
async def send_welcome(message: Message):
    await rq.set_user(message.from_user.id, message.chat.id, message.from_user.full_name)
    #chat_id = message.chat.id
    #user_id = message.from_user.id
    await message.answer(f'Привет, {message.from_user.full_name}!' , reply_markup=kb.main)
    await message.answer(f"Вас приветствует бот актуальных скидок, в данном чате Вы будете получать сообщения о текущих скидках в интернет-магазинах.\n\n"
                         f"Для того, чтобы сообщения о скидках начали Вам приходить пожалуйста нажмите на кнопку 'Категории' и выберите на какие категории товаров вас интересуют скидки.")

@router.message(F.text == 'Категории')
async def open_category(message: Message):
    await message.answer('Выберите категорию на которую хотите подписаться', reply_markup= await kb.categories())

@router.message(F.text == 'О нас')
async def about_us(message: Message):
    await message.answer('Мы команда 21-КТ сделали Чат бота отслеживающий скидки')

@router.message(F.text == 'Мои категории')
async def write_my_category(message: Message):
    subscriptions = await rq.get_subscriptions()
    user_subscriptions = [sub.category_name for sub in subscriptions if sub.tg_id == message.from_user.id]

    # Проверяем, есть ли категории
    if user_subscriptions:
        categories = "\n".join(user_subscriptions)
        await message.answer(f"Ваши категории:\n{categories}", reply_markup=kb.main)
    else:
        await message.answer("У вас нет подписок на категории.", reply_markup=kb.main)



@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    category_id = int(callback.data.split('_')[1])
    
    
    # Получаем категорию из БД по id
    category = await get_category_by_id(category_id)
    print(category.name)
    if await rq.set_user_category(callback.from_user.id, category.name):
        await callback.answer(f'Вы выбрали категорию "{category.name}"')   
        await callback.message.answer(f'Вы подписались на категорию "{category.name}"')
    else:
        await callback.message.answer(f'Уже подписаны на "{category.name}"', reply_markup= await kb.delete_user_category(category.name))


@router.callback_query(F.data.startswith('to_main'))
async def write_my_category(callback: CallbackQuery):
    subscriptions = await rq.get_subscriptions()
    user_subscriptions = [sub.category_name for sub in subscriptions if sub.tg_id == callback.from_user.id]

    # Проверяем, есть ли категории
    if user_subscriptions:
        categories = "\n".join(user_subscriptions)
        await callback.message.answer(f"Ваши категории:\n{categories}", reply_markup=kb.main)
    else:
        await callback.message.answer("У вас нет подписок на категории.", reply_markup=kb.main)

@router.callback_query(F.data.startswith('delete_user_category_'))
async def write_my_category(callback: CallbackQuery):
    subscriptions = await rq.get_subscriptions()
    category_name = callback.data[len('delete_user_category_'):]
    subscription_to_delete = None
    for subscription in subscriptions:
        if subscription.tg_id == callback.from_user.id and subscription.category_name == category_name:
            subscription_to_delete = subscription
            break

    if subscription_to_delete:
        # Удаляем запись
        await rq.delete_user_category(subscription_to_delete.tg_id, subscription_to_delete.category_name)
        await callback.answer(f"Категория '{category_name}' была удалена.", reply_markup=kb.main)
    else:
        await callback.answer(f"Вы не подписаны на категорию '{category_name}'.", reply_markup=kb.main)
