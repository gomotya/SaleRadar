import requests
from bs4 import BeautifulSoup
from notifier import process_product

BASE_URL = "https://nn.istoreapple.ru/smartfony-iphone/?page={page}"

async def parse(session):
    page_number = 1
    while True:
        page_url = BASE_URL.format(page=page_number)
        if not await parse_page(page_url, session) or page_number == 2:
            break
        page_number += 1

    print("Парсинг завершён.")

async def parse_page(url, session):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    category = "Телефоны"
    shop_name = "istore.ru"

    items = soup.select(".product_item")
    if not items:
        return False

    for item in items:
        name = item.select_one("h3").text.strip() if item.select_one("h3") else None
        if not name:
            continue

        price_tag = item.select_one(".new_price")
        price = clean_price(price_tag.text) if price_tag else None

        link_div = item.select_one(".product_link")
        # Извлекаем <a> внутри блока product_link
        link_tag = link_div.find('a') if link_div else None
        link = link_tag['href'].strip() if link_tag and link_tag.get('href') else None
        print(f"{name}\n{category}\n{price}\n{link}\n{shop_name}\n")
        await process_product(session, name, category, price, link, shop_name)

    return True

def clean_price(price_text):
    try:
        return int(price_text.replace("₽", "").replace(" ", "").replace("\xa0", ""))
    except ValueError:
        return None