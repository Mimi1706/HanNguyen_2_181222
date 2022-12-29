import requests
from bs4 import BeautifulSoup
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
            page_url = 'http://books.toscrape.com/catalogue/category/books/{0}/page-{1}.html'.format(category,page) ## iterates through pages
            response = requests.get(page_url)
            soup = BeautifulSoup(response.text, "html.parser") ## parser type
            book_infos = soup.find_all("article", {"class": "product_pod"}) ## finds all books components

            for book in book_infos:
                book_url = "http://books.toscrape.com/catalogue/" + '/'.join(book.find("a")['href'].split('/')[3:]) ## url of the book
                books_urls.append(book_url)

    else: ## else this category only has one page
        page_url = 'http://books.toscrape.com/catalogue/category/books/{0}/index.html'.format(category) ## iterates through pages
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, "html.parser") ## parser type
        book_infos = soup.find_all("article", {"class": "product_pod"}) ## finds all books components

        for book in book_infos:
            book_url = "http://books.toscrape.com/catalogue/" + '/'.join(book.find("a")['href'].split('/')[3:]) ## url of the book without the "../../../" at the beginning of the path
            books_urls.append(book_url)

    return books_urls

def get_book_infos(book_url):
    response = requests.get(book_url) ## gets to the book url
    soup = BeautifulSoup(response.text, "html.parser") 

    ## retrieves the following data:
    title = '_'.join(e for e in soup.find("h1").text.lower().split(' ') if e.isalnum()) ## filters all the special characters to avoid errors when saving the image name
    image_url = "http://books.toscrape.com/" + soup.find("img")['src'].split('/',2)[-1]

    return title, image_url

def get_images():  
    if not os.path.exists("./images"):
        os.makedirs("./images") ## creates the books folder  
    for category in get_categories():
        if not os.path.exists("./images/{0}".format(category)):
            os.makedirs("./images/{0}".format(category)) ## creates the category folder
        for book in get_books_urls(get_categories()[category]):
            img_data = requests.get(get_book_infos(book)[1]).content ## retrieves the image content via the url
            with open('./images/{0}/{1}.jpg'.format(category,get_book_infos(book)[0]), 'wb') as image_file:
                image_file.write(img_data) ## saves the image
    return
    
get_images()