import requests
from bs4 import BeautifulSoup
from notifier import process_product 

BASE_URL = "https://printbar.ru/futbolki/"
async def parse(cursor):
    page_number = 1
    while True:
        page_url = f"{BASE_URL}?p={page_number}"
        if not await parse_page(page_url, cursor) or page_number == 3:
            break
        page_number += 1

    print("Парсинг printbar.ru завершён.")

async def parse_page(url, cursor):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    category = "Футболки"
    shop_name = "printbar.ru"
    items = soup.select(".pb__catalog--product-item--block")  # Класс карточки товара на сайте
    if not items:
        return False
    
    for item in items:
        name = item.select_one(".pb__catalog--cproduct-info--title").text.strip()  # Название товара
        price_tag = item.select_one(".pb__catalog--cproduct-info--price")  # Цена товара
        if price_tag:
            spans = price_tag.find_all("span")  # Находим все <span> внутри контейнера
            if len(spans) > 1:
                second_span_text = spans[1].text.strip()  # Берём текст второго <span>
            else:
                second_span_text = None  # Если второго <span> нет
        else:
            second_span_text = None
        price = parse_price(second_span_text if second_span_text else "0")
        link = parse_link(item)
        print(f"{name}\n{category}\n{price}\n{link}\n{shop_name}\n")  
        await process_product(cursor, name, category, price, link, shop_name)  
    return True

def parse_price(price_text):
    try:
        return int(price_text.replace("₽", "").replace(" ", "").strip())
    except ValueError:  
        return None

def parse_link(item):
    link_tag = item.select_one(".pb__catalog--product-item--link")  # Ссылка на товар
    return f"{link_tag['href'].strip()}" if link_tag and link_tag.get('href') else None