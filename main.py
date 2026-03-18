import requests
from bs4 import BeautifulSoup
import urllib3
import time
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

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

with open('books.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Price', 'Availability'])

    while url:
        # 3. Use the headers in the request
        response = requests.get(url, headers=headers, verify=False)
        
        # 4. Use .content instead of .text to avoid the "A" symbol bug
        soup = BeautifulSoup(response.content, "html.parser")

        print(f"Scraping: {url}")
        
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            stock = book.find("p", class_="instock availability").text.strip()
            writer.writerow([title, price, stock])

        # 5. Add a small delay so you don't look like a spammer
        time.sleep(1) 

        next_button = soup.find("li", class_="next")
        if next_button:
            next_page_rel = next_button.a["href"]
            url = "https://books.toscrape.com/catalogue/" + next_page_rel
        else:
            url = None