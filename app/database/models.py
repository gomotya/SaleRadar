from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
engine = create_async_engine(url=os.getenv('BD_URL'))

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    chat_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(512))

class Subscription(Base):
    __tablename__ = 'subscriptions'
    
    id_subscription: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(512))
    tg_id = mapped_column(BigInteger)

class Category(Base):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))

class Product(Base):
    __tablename__ = 'products'
    
    id_product: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(512))
    category: Mapped[str] = mapped_column(String(512))
    price: Mapped[int] = mapped_column()
    link: Mapped[str] = mapped_column(String(512))
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    shop_name: Mapped[str] = mapped_column(String(512))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)