import requests
from bs4 import BeautifulSoup
from notifier import process_product

BASE_URL = "https://sneakerhead.ru/shoes/"


async def parse(cursor):
    page_number = 1  # Начать с первой страницы
    while True:
        page_url = f"{BASE_URL}?PAGEN_2={page_number}"
        print(f"Парсинг страницы: {page_url}")
        if not await parse_page(page_url,cursor) or page_number == 6:  # Если товаров нет, завершаем парсинг
            break
        page_number += 1

    print("Парсинг sneakerhead.ru завершён.")


async def parse_page(url, cursor):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Ошибка загрузки страницы: {url}")
        return False

    soup = BeautifulSoup(response.text, "html.parser")
    category = "Обувь"
    shop_name = "sneakerhead.ru"

    # Ищем все элементы с товарами
    items = soup.select(".product-cards__item")  # Класс карточки товара на сайте SneakerHead
    if not items:
        return False  # Если товаров нет, завершаем парсинг страницы

    for item in items:
        # Название товара
        name_tag = item.select_one(".product-card__title")
        name = name_tag.text.strip() if name_tag else "Без названия"


        # Цена товара
        price_tag = item.select_one(".product-card__price-value")
        price = price_tag.text.strip() if price_tag else "Без названия"
        price = price.replace("₽", "").replace(" ", "").replace("\xa0", "").strip()
        price=int(price)
        # Ссылка на товар
        link = parse_link(item)
        url = link.rstrip("/")
        dlina = url[-8:]
        name = name+' '+dlina
        # Вывод информации
        print(f"{name}\n{category}\n{price}\n{link}\n{shop_name}\n")
        await process_product(cursor, name, category, price, link, shop_name)
    return True


def parse_price(price_text):
    try:
        return int(price_text.replace(" ", ""))  # Преобразуем цену в float
    except ValueError:
        return None  # Если не удалось преобразовать цену, возвращаем None


def parse_link(item):
    link_tag = item.select_one(".product-card__title a")  # Ссылка на товар
    href = link_tag.get("href") if link_tag else "#"
    return f"https://sneakerhead.ru{href}"

