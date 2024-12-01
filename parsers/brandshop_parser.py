import requests
from bs4 import BeautifulSoup
from notifier import process_product 

BASE_URL = "https://brandshop.ru/muzhskoe/odezhda/futbolki/"

async def parse(cursor):
    page_number = 1  # Начать с первой страницы
    while True:
        page_url = f"{BASE_URL}?page={page_number}"
        print(f"Парсинг страницы: {page_url}")
        if not await parse_page(page_url, cursor):  # Если товаров нет, завершаем парсинг
            break
        page_number += 1

    print("Парсинг brandshop.ru завершён.")

async def parse_page(url, cursor):
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, "html.parser")
    category = "Футболки"
    shop_name = "brandshop.ru"

    # Ищем все элементы с товарами
    items = soup.select(".product-card")  # Класс карточки товара на сайте
    #print(items)
    if not items:
        return False  # Если товаров нет, завершаем парсинг страницы
    
    for item in items:
        # Название товара
        name = item.select_one(".product-card__title")
        c = name.select_one("span")
        c2 = name.find_all("div")
        dc = c2[1]

        name = c.text.strip() + " " + dc.text.strip()
     
        link_tag = item.select_one(".product-card__price")  # Ссылка на товар
        lt = link_tag.find('link')
        href = lt.get('href')
        q = href[7:]
        name = name + " " + q[:6]
        # Цена товара
        price_tag = item.select_one(".product-card__price")  
        c = price_tag.find_all("meta")
        dc = c[1].get('content')
    

        price = parse_price(dc if dc else "0")  # Парсим цену

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
    link_tag = item.select_one(".product-card__price")  # Ссылка на товар
    lt = link_tag.find('link')
    href = lt.get('href')

    return f"https://brandshop.ru{href}"