import requests
from bs4 import BeautifulSoup
import urllib3

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# url = "https://books.toscrape.com/"
# response = requests.get(url)
# # response = requests.get(url, verify=False)

# soup = BeautifulSoup(response.text, "html.parser")

# # print(soup)

# books = soup.find_all("article", class_="product_pod")

# # print(len(books))

# for book in books:
#     title = book.h3.a["title"]
#     price = book.find("p", class_="price_color").text
#     inStockOrNot = book.find("p", class_="instock availability").text.strip()

#     print(f"{title} > {price} > {inStockOrNot}")

# print("------------")

url = "https://books.toscrape.com/catalogue/page-1.html"

while url:
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")

    print(f"Scraping: {url}")
    print("----------")

    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        inStockOrNot = book.find("p", class_="instock availability").text.strip()
        print(f"{title} > {price} > {inStockOrNot}")
    print("-----------")

    next_button = soup.find("li", class_="next")

    if next_button:
        next_page_rel = next_button.a["href"]
    
        url = "https://books.toscrape.com/catalogue/" + next_page_rel

    else:
        url = None