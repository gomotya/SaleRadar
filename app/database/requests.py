from app.database.models import async_session
from app.database.models import User, Category, Subscription
from sqlalchemy import select
from bot_instance import bot

async def set_user(tg_id: int, chat_id: int, name: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id, User.chat_id == chat_id, User.name == name))

        if not user:
            session.add(User(tg_id=tg_id, chat_id=chat_id, name=name))
            await session.commit()
        if not user:
            await bot.send_message(
                    553450853, 
                    f"Новый пользователь зарегистрирован:\nID: {tg_id}\nChat ID: {chat_id}"
        )

async def set_user_category(tg_id: int, category: str) -> None:
    async with async_session() as session:
        subscription = await session.scalar(select(Subscription).where(Subscription.tg_id == tg_id, Subscription.category_name == category))

        if not subscription:
            session.add(Subscription(tg_id=tg_id, category_name=category))
            await session.commit()
            return True
        else:
            return False

async def delete_user_category(tg_id: int, category: str) -> None:
    async with async_session() as session:
        # Ищем подписку, которую нужно удалить
        subscription = await session.scalar(select(Subscription).where(Subscription.tg_id == tg_id, Subscription.category_name == category))

        if subscription:
            # Если подписка найдена, удаляем ее
            await session.delete(subscription)
            await session.commit()
            return True
        else:
            return False        

async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))
    
async def get_subscriptions():
    async with async_session() as session:
        return await session.scalars(select(Subscription))
    



async def get_all_tg_ids() -> list[int]:
    async with async_session() as session:
        # Запрос на получение всех tg_id пользователей
        result = await session.execute(select(User.tg_id))
        tg_ids = result.scalars().all()  # Извлекаем все tg_id в виде списка
        return tg_ids
    
async def get_category_by_id(category_id: int):
    # Предполагается, что get_categories() возвращает список объектов категорий.
    # Если вы используете SQLAlchemy, вы можете адаптировать запрос соответственно.
    all_categories = await get_categories()
    return next((cat for cat in all_categories if cat.id == category_id), None)    