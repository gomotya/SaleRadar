import requests
from bs4 import BeautifulSoup
from notifier import process_product

BASE_URL = "https://www.svyazon.ru/catalog/phone/225/apple/page-{page}/"

async def parse(session):
    page_number = 1
    while True:
        page_url = BASE_URL.format(page=page_number)
        if not await parse_page(page_url, session):
            break
        page_number += 1

    print(f"Парсинг завершён.")

async def parse_page(url, session):
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    })
    if response.status_code != 200:
        print(f"Ошибка при загрузке страницы {url}")
        return False

    soup = BeautifulSoup(response.text, "html.parser")
    category = "Телефоны"
    shop_name = "svyazon.ru"

    items = soup.select("article[data-product-card]")
    if not items:
        return False
    
    for item in items:
        name = item.select_one(".s-product-card-name__link").text.strip() if item.select_one(".s-product-card-name__link") else None
        if not name or name == 'Apple iPhone 16 Pro 256 Гб eSIM + SIM (белый титан)':
            continue

        price_tag = item.select_one(".s-product-card-price")
        price = clean_price(price_tag.text) if price_tag else None

        link_tag = item.select_one(".s-product-card-name__link")
        link = "https://www.svyazon.ru" + link_tag['href'].strip() if link_tag and link_tag.get('href') else None

        print(f"{name}\n{category}\n{price}\n{link}\n{shop_name}\n")
        await process_product(session, name, category, price, link, shop_name)

    return True

def clean_price(price_text):
    try:
        return int(price_text.replace("₽", "").replace(" ", "").replace("\xa0", ""))
    except ValueError:
        return None