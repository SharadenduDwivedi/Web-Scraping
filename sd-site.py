import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

url = "https://www.sharadendu-dwivedi.vercel.app"

# response = requests.get(url)
response = requests.get(url, headers=headers, verify=False)

soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a")

for link in links:
    print(f"{link.text} : {link['href']}")
