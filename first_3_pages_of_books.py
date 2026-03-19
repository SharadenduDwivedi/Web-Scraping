import requests
from bs4 import BeautifulSoup
import urllib3
import csv
from urllib.parse import urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

with open('first_3_pages_books.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Price', 'Star Rating','URL'])

    n = 1
    while n < 4:
        url = f"https://books.toscrape.com/catalogue/page-{n}.html"
        response = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(response.content, "html.parser")

        book_container = soup.find_all("article", class_="product_pod")

        print(f"Scraping page{n}")
        for book in book_container:
            title = book.h3.a['title']
            price =  book.find("p", class_="price_color").text
            rating_scale = ["One", "Two","Three","Four","Five"]
            rating = book.find("p", class_= "star-rating")
            rating_value = rating['class'][1]
            for r in rating_scale:
                if r == rating_value:
                    rating_value = rating_scale.index(r)+1
            product_url = urljoin(url, book.h3.a['href'])
            writer.writerow([title, price, rating_value, product_url])
        
        n+=1

print("File Created")