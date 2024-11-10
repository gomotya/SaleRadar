import requests
from bs4 import BeautifulSoup

def parse_products():
    url = "https://kolosstore.ru/product-category/носки/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for item in soup.select(".product-item"):
        name = item.select_one(".product-title").text.strip()
        price = int(item.select_one(".product-price").text.strip().replace("₽", "").replace(" ", ""))
        link = item.select_one("a")["href"]
        products.append({"name": name, "price": price, "link": link})

    return products
