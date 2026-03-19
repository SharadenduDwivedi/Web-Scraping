import requests
from bs4 import BeautifulSoup
import urllib3
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

url = "https://quotes.toscrape.com/"

with open('quotes.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['Quote', 'Author', 'Author_URL','Tags'])

    while url:
        response = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(response.content, "html.parser")

        quote_div = soup.find_all("div", class_="quote")

        for quotes in quote_div:
            quote_text = quotes.find("span", class_="text").text
            quote_author = quotes.find("small", class_="author").text
            author_link = "https://quotes.toscrape.com" + quotes.a['href']
            tags = []
            tag_div = quotes.find("div", class_="tags")

            tag = tag_div.find_all("a", class_="tag")

            for t in tag:
                tags.append(t.text)

            tags = ' '.join(tags)

            writer.writerow([quote_text, quote_author, author_link, tags])

        next_button = soup.find("li", class_="next")

        if next_button:
            url = "https://quotes.toscrape.com" + next_button.a['href']
        else:
            url = None
print("CSV file created!")