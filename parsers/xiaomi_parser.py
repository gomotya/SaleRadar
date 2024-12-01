import requests
from bs4 import BeautifulSoup
from notifier import process_product

# Глобальные переменные для отслеживания текущей страницы и максимального количества страниц
current_page = 1
max_pages = 6  # Максимальное количество страниц для парсинга

BASE_URL = "https://mi-shop.com/catalog/smartphones/?PAGEN_1={page}"

async def parse(session):
    global current_page

    while current_page <= max_pages:
        page_url = BASE_URL.format(page=current_page)
        if not await parse_page(page_url, session):
            break
        current_page += 1

    print("Парсинг завершён.")

async def parse_page(url, session):
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    })

    if response.status_code != 200:
        print(f"Ошибка при загрузке страницы {url}")
        return False

    soup = BeautifulSoup(response.text, "html.parser")
    category = "Телефоны"
    shop_name = "mi-shop.com"

    items = soup.select(".b-catalog__column")

    if not items:  # Если товаров на странице нет
        print(f"На странице {url} товаров не найдено.")
        return False

    for item in items:
        # Извлечение имени
        name_tag = item.select_one(".b-product-card__title")
        name = name_tag.text.strip() if name_tag else None
        if not name:
            continue

        # Извлечение цены
        price_tag = item.select_one(".js-stats-price-new")
        price = clean_price(price_tag.text) if price_tag else None

        # Извлечение ссылки
        link_tag = item.select_one("a[href]")
        link = "https://mi-shop.com" + link_tag['href'].strip() if link_tag and link_tag.get('href') else None

        print(f"{name}\n{category}\n{price}\n{link}\n{shop_name}\n")
        await process_product(session, name, category, price, link, shop_name)

    return True

def clean_price(price_text):
    """Очистка цены от лишних символов и преобразование в float"""
    try:
        return int(price_text.replace("₽", "").replace(" ", "").replace("\xa0", ""))
    except ValueError:
        return None

# Запуск парсинга
if __name__ == "__main__":
    parse()
