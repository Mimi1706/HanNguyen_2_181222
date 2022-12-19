import requests
from bs4 import BeautifulSoup
import csv

url = 'http://books.toscrape.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

pages_count = int(soup.find("li", {"class": "current"}).text.split()[-1])

books_infos = soup.findAll('article', {"class": "product_pod"})

