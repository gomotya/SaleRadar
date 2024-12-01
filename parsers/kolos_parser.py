import requests
from bs4 import BeautifulSoup
from notifier import process_product

BASE_URL = "https://kolosstore.ru/product-category/носки/"

async def parse(cursor):
    page_number = 1
    while True:
        page_url = f"{BASE_URL}page/{page_number}/"
        if not await parse_page(page_url, cursor):
            break
        page_number += 1

    print("Парсинг kolosstore завершён.")

async def parse_page(url, cursor):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    category = "Носки"
    shop_name = "kolosstore.ru"

    items = soup.select(".product")
    if not items:
        return False

    for item in items:
        name = item.select_one(".woocommerce-loop-product__title").text.strip()
        if "носки" not in name.lower():
            continue

        price_tag = item.select(".price bdi")
        price = parse_price(price_tag)
        link = parse_link(item)
        print(f"{name}\n{category}\n{price}\n{link}\n{shop_name}\n")
        await process_product(cursor, name, category, price, link, shop_name)
    return True

def parse_price(price_tag):
    if len(price_tag) > 1:
        return clean_price(price_tag[1].text)
    elif price_tag:
        return clean_price(price_tag[0].text)
    return None

def clean_price(price_text):
    try:
        return int(price_text.replace("₽", "").replace(" ", ""))
    except ValueError:
        return None

def parse_link(item):
    link_tag = item.select_one("a")
    return link_tag['href'].strip() if link_tag and link_tag.get('href') else None


