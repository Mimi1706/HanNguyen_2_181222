import requests
from bs4 import BeautifulSoup
import csv

def get_all_books_urls():
    url = "http://books.toscrape.com/index.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser") ## parser type

    total_pages = int(soup.find("li", {"class": "current"}).text.split()[-1])
    book_infos = soup.find_all("article", {"class": "product_pod"})
    books_urls = []

    for page in range(1,total_pages+1):
        url = 'http://books.toscrape.com/catalogue/page-{0}.html'.format(page)

        for book in book_infos:
            book_url = "http://books.toscrape.com/" + book.find("a")['href']
            books_urls.append(book_url)
    
    return books_urls

def get_book_infos(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, "html.parser")

    product_page_url = book_url
    universal_product_code = soup.find_all("td")[0].text
    title = soup.find("h1").text
    price_including_tax = soup.find_all("td")[3].text
    price_excluding_tax = soup.find_all("td")[2].text
    number_available = soup.find_all("td")[5].text
    product_description = soup.find("article", {"class":"product_page"}).find_all("p")[3].text
    category = soup.find("ul", {"class":"breadcrumb"}).find_all("a")[2].text
    review_rating = soup.find("p", {"class":"star-rating"})['class'][-1]
    image_url = "http://books.toscrape.com/" + soup.find("img")['src'].split('/',2)[-1]

    product_infos_type = [product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url]

    return product_infos_type

def write_csv():
    en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]

    with open("books.csv", "w", newline="") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=",")
        writer.writerow(en_tete)
        for book in get_all_books_urls():
            writer.writerow(get_book_infos(book))
    
write_csv()
        