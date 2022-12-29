import requests
from bs4 import BeautifulSoup
import os ## to create a directory

page_url = "" ## paste the page link inside "" example: "http://books.toscrape.com/catalogue/category/books/childrens_11/page-2.html"

def get_books_urls():
    response = requests.get(page_url)
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

    ## retrieves the following data:
    title = '_'.join(e for e in soup.find("h1").text.lower().split(' ') if e.isalnum()) ## filters all the special characters to avoid errors when saving the image name
    image_url = "http://books.toscrape.com/" + soup.find("img")['src'].split('/',2)[-1]

    return title, image_url

def get_images():
    if not os.path.exists("./images"):
        os.makedirs("./images") ## creates the books folder  
    for book in get_books_urls():
        img_data = requests.get(get_book_infos(book)[1]).content ## retrieves the image content via the url
        with open('./images/{0}.jpg'.format(get_book_infos(book)[0]), 'wb') as image_file:
            image_file.write(img_data) ## saves the image
    return

get_images()