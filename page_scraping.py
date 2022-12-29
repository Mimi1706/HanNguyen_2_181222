import requests
from bs4 import BeautifulSoup
import csv

url = "" ## paste the page link inside "" example: "http://books.toscrape.com/catalogue/category/books/childrens_11/page-2.html"

def get_books_urls():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser") ## parser type

    book_infos = soup.find_all("article", {"class": "product_pod"})
    books_urls = []

    for book in book_infos:
        book_url = "http://books.toscrape.com/catalogue/" + '/'.join(book.find("a")['href'].split('/')[3:]) ## url of the book
        books_urls.append(book_url)
    
    return books_urls

def get_book_infos(book_url):
    response = requests.get(book_url) ## gets to the book url
    soup = BeautifulSoup(response.text, "html.parser") 

    ## retrieves the following data
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

    return product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url

def write_csv():
    en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]

    with open("books-to-scrape.csv", "w", newline="") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=",") ## defines the writing method
        writer.writerow(en_tete) ## writes the columns title
        for book in get_books_urls(): ## writes the retrieved data in each column
            writer.writerow(get_book_infos(book))
    
write_csv()