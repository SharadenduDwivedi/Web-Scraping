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

navigationLinks = soup.find("div", class_="pages")

links = navigationLinks.find_all("a")

for link in links:
    if link['href'] != "":
        print(link.text)
    else:
        print("Nothing")

        
# headings = soup.find_all("h1")

# print("-"*6,"Printing Headings","-"*6)
# for heading in headings:
#     print(heading.text)
# print("-"*6,"Headings Printed","-"*6)

# links = soup.find_all("a")

# print("-"*6,"Printing Links","-"*6)
# for link in links:
#     img = link.find("img")

#     if img and img.has_attr('alt'):
#         print(img['alt'])
#     else:
#         print(link.text)
# print("-"*6,"Links Printed","-"*6)