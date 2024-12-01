import requests
from bs4 import BeautifulSoup
from notifier import process_product 

BASE_URL = "https://zarina.ru/catalog/clothes/futbolki/"

async def parse(cursor):
    page_number = 2  # Начать с первой страницы
    while True:
        page_url = f"{BASE_URL}?page={page_number}"
        print(f"Парсинг страницы: {page_url}")
        if not await parse_page(page_url, cursor):  # Если товаров нет, завершаем парсинг
            break
        page_number += 1

    print("Парсинг zarina.ru завершён.")

async def parse_page(url, cursor):
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, "html.parser")
    category = "Футболки"
    shop_name = "zarina.ru"

    # Ищем все элементы с товарами
    items = soup.select(".catalog__item")  # Класс карточки товара на сайте
    if not items:
        return False  # Если товаров нет, завершаем парсинг страницы
    
    for item in items:
        # Название товара
        name = item.select_one(".catalog__product-title")
        c = item.find_all("meta")
        dc = c[1].get('content')
        name = name.text.strip() if name else 'Без названия'
        name = name + " " + dc
        # Цена товара
        price_tag = item.select_one(".catalog__product-price_current")  

        price = parse_price(price_tag.text if price_tag else "0")  # Парсим цену

        # Ссылка на товар
        link = parse_link(item)
        
        # Вывод информации
        print(f"{name}\n{category}\n{price}\n{link}\n{shop_name}\n")
        await process_product(cursor, name, category, price, link, shop_name)
    return True

def parse_price(price_text):
    try:
        return int(price_text.replace("₽", "").replace(" ", "").strip())  # Преобразуем цену в float
    except ValueError:
        return None  # Если не удалось преобразовать цену, возвращаем None

def parse_link(item):
    link_tag = item.select_one(".catalog__product-title")  # Ссылка на товар
    lt = link_tag.find('a')
    href = lt.get('href')

    return f"https://zarina.ru{href}"