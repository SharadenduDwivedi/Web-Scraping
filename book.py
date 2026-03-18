import requests
from bs4 import BeautifulSoup
import csv
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

url = "https://books.toscrape.com/catalogue/page-1.html"

# CHANGE: Use 'utf-8-sig' here to fix Excel's display issues
with open('books.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Price', 'Availability'])

    while url:
        # Use headers to bypass the firewall
        response = requests.get(url, headers=headers, verify=False)
        
        # CHANGE: Use .content (raw bytes) so BeautifulSoup can handle the "A" symbol logic for us
        soup = BeautifulSoup(response.content, "html.parser")

        print(f"Scraping: {url}")

        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            stock = book.find("p", class_="instock availability").text.strip()
            
            writer.writerow([title, price, stock])

        next_button = soup.find("li", class_="next")
        if next_button:
            next_page_rel = next_button.a["href"]
            url = "https://books.toscrape.com/catalogue/" + next_page_rel
        else:
            url = None

print("File 'books.csv' has been created successfully!")