import requests
from bs4 import BeautifulSoup
from notifier import process_product

BASE_URL = "https://www.noone.ru/catalog/zhenskoe/obuv/"


async def parse(cursor):
    page_number = 1  # Начать с первой страницы
    while True:
        page_url = f"{BASE_URL}?PAGE={page_number}"  # Формат пагинации сайта
        if not await parse_page(page_url, cursor) or page_number == 5:  # Если товаров нет, завершаем парсинг
            break
        page_number += 1

    print("Парсинг noone.ru завершён.")


async def parse_page(url, cursor):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Ошибка загрузки страницы: {url}")
        return False

    soup = BeautifulSoup(response.text, "html.parser")
    category = "Обувь"
    shop_name = "noone.ru"

    # Ищем все элементы с товарами
    items = soup.select(".col.lg\\:col-4.xs\\:col-6")
    if not items:
        return False  # Если товаров нет, завершаем парсинг страницы

    for item in items:
        # Название товара
        name_tag = item.select_one(".item-brand")
        name = name_tag.text.strip() if name_tag else "Без названия"

        # Цена товара
        price_tag = item.select_one(".item-price-new.text-data")
        price = price_tag.text.strip() if price_tag else "Без названия"
        price = price.replace(" ", "").replace("\xa0", "").replace("₽", "").strip()
        price = int(price)
        # Ссылка на товар
        link = parse_link(item)
        url = link.rstrip("/")
        dlina = url[-6:]
        name = name + ' ' + dlina
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
    link_tag = item.select_one(".item-link.js-item-link")
    if link_tag is None or not link_tag.get('href'):
        return None

    # Формирование полного URL
    href = link_tag.get('href')
    return f"https://www.noone.ru{href}"


