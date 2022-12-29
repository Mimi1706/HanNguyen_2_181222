import requests
from bs4 import BeautifulSoup
import csv
import os ## to create a directory

def get_categories():
    all_categories = {}
    url = "http://books.toscrape.com/index.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser") ## parser type
    categories = soup.find("ul", {"class":"nav-list"}).find_all("a")

    for category in range(1, len(categories)):
        category_name = categories[category].get_text(strip=True).lower()
        all_categories[category_name] = "-".join(category_name.split(' ')) + '_' + str(category+1)

    return all_categories

def get_books_urls(category):
    url = "http://books.toscrape.com/catalogue/category/books/{0}".format(category)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser") ## parser type
    books_urls = []

    if soup.find("li", {"class": "current"}) is not None: ## if there are multiple pages
        total_pages = int(soup.find("li", {"class": "current"}).text.split()[-1]) ## total number of pages at the bottom of the page
        for page in range(1,total_pages+1):
            page_url = 'http://books.toscrape.com/catalogue/category/books/{0}/page-{1}.html'.format(category,page) ## read through pages
            response = requests.get(page_url)
            soup = BeautifulSoup(response.text, "html.parser") ## parser type
            book_infos = soup.find_all("article", {"class": "product_pod"}) ## find all books components

            for book in book_infos:
                book_url = "http://books.toscrape.com/catalogue/" + '/'.join(book.find("a")['href'].split('/')[3:]) ## url of the book
                books_urls.append(book_url)

    else: 
        page_url = 'http://books.toscrape.com/catalogue/category/books/{0}/index.html'.format(category) ## read through pages
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, "html.parser") ## parser type
        book_infos = soup.find_all("article", {"class": "product_pod"}) ## find all books components

        for book in book_infos:
            book_url = "http://books.toscrape.com/catalogue/" + '/'.join(book.find("a")['href'].split('/')[3:]) ## url of the book
            books_urls.append(book_url)

    return books_urls

def get_book_infos(book_url):
    response = requests.get(book_url) ## get to the book url
    soup = BeautifulSoup(response.text, "html.parser") 

    ## retrieve the data
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

def get_all_books():
    en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
    if not os.path.exists("./books-to-scrape"):
        os.makedirs("./books-to-scrape") ## makes books folder

    for category in get_categories():
        with open("./books-to-scrape/{0}_books.csv".format(''.join(get_categories()[category].split('_')[:-1])), "w", newline="") as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=",") ## define the writing method
            writer.writerow(en_tete) ## write the columns title
            for book in get_books_urls(get_categories()[category]): ## write the retrieved data in each column
                writer.writerow(get_book_infos(book))

    return
    
get_all_books()