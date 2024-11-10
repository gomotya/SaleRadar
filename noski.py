import requests
from bs4 import BeautifulSoup
import psycopg2
import asyncio
from datetime import datetime
from bot_instance import bot
from app.database.requests import get_all_tg_ids  



# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="salesbot",  
    user="postgres",    
    host="localhost", 
    password="1234",      
    port="5432",        
    options="-c client_encoding=UTF8"                            
)
cursor = conn.cursor()

# Базовый URL для данного сайта в категории носки
base_url = "https://kolosstore.ru/product-category/носки/"

async def notify(text_message):
    tg_ids = await get_all_tg_ids()
    for tg_id in tg_ids:
        await bot.send_message(553450853, f"Сообщение было доставлено {tg_id}")
        await bot.send_message(tg_id, text_message)


def parse_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    category = "носки"  
    shop_name = "kolosstore.ru"  
    
    items = soup.select(".product")
    # Парсим названия и цены товаров на странице
    if not items:
        return False  # Если товаров на странице нет, завершаем парсинг

    for item in items:
        name = item.select_one(".woocommerce-loop-product__title").text.strip()

        if "носки" not in name.lower():
            continue

        price_tag = item.select(".price bdi")
        if len(price_tag) > 1:
            # Если тегов <bdi> два, берем второй
            price = price_tag[1].text.strip().replace("₽", "").replace(" ", "")
        elif price_tag:
            # Если тегов <bdi> только один, берем его
            price = price_tag[0].text.strip().replace("₽", "").replace(" ", "")
        else:
            price = None  # Если тег <bdi> не найден, оставляем цену как None

        # Преобразуем цену в числовой формат, если удалось
        try:
            price = float(price)  # Приводим к числу
        except ValueError:
            price = None  # Если не удалось привести к числу, оставляем как None
        link = item.select_one("a")
        if link and link.get('href'):
            link = link['href'].strip()
        else:
            link = None  # Если ссылка отсутствует, устанавливаем NULL
        cursor.execute("SELECT id_product, price FROM products WHERE name = %s AND shop_name = %s", (name, shop_name))
        existing_product = cursor.fetchone()

        if existing_product:
            product_id, existing_price = existing_product
            if existing_price > price:
                
                 # Отправка сообщения в боте о понижении цены
                message_text = (
                    f"Цена товара '{name}' уменьшилась.\n"
                    f"Старая цена: {existing_price}\n"
                    f"Новая цена: {price}\n"
                    f"Ссылка на товар: {link}"
            )
            # Отправляем сообщение администратору
                asyncio.run(notify(message_text))
            # Если цена изменилась, обновляем цену в базе данных
            if existing_price != price:
                cursor.execute("""
                    UPDATE products 
                    SET price = %s, date = %s 
                    WHERE id_product = %s
                """, (price, datetime.now().date(), product_id))
                print(f"Цена товара '{name}' изменена с {existing_price} на {price}.")
            else:
                print(f"Цена товара '{name}' не изменилась.")
        else:
            # Если товар не найден в базе, добавляем новый
            cursor.execute("""
                INSERT INTO products (name, category, price, link, date, shop_name)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, category, price, link, datetime.now().date(), shop_name))
            print(f"Добавлен новый товар: '{name}' с ценой {price}.")
    return True

# Переходим по страницам с товарами
page_number = 1
while True:
    page_url = f"https://kolosstore.ru/product-category/носки/page/{page_number}/"
    if not parse_page(page_url):
        break  # Останавливаем цикл, если товаров больше нет на странице
    print(f"Страница {page_url} обработана.")
    # Пытаемся найти ссылку на следующую страницу
    page_number += 1

# Сохраняем изменения и закрываем соединение
conn.commit()
cursor.close()
conn.close()


print("Парсинг всех страниц и запись в БД завершены.")



  