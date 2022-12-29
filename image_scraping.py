import requests
from bs4 import BeautifulSoup
import os ## to create a directory

book_url = "" ## paste the book link inside "" example: "http://books.toscrape.com/catalogue/the-cat-in-the-hat-beginner-books-b-1_235/index.html"

def get_image_url(book_url):
    response = requests.get(book_url) ## get to the book url
    soup = BeautifulSoup(response.text, "html.parser") 
    ## retrieve the image
    image_url = "http://books.toscrape.com/" + soup.find("img")['src'].split('/',2)[-1]
    title = '_'.join(soup.find("h1").text.lower().split(' '))

    return image_url, title

def save_image(image_url, title):
    if not os.path.exists("./images"):
        os.makedirs("./images") ## makes books folder

    img_data = requests.get(image_url).content
    with open('./images/{0}.jpg'.format(title), 'wb') as handler:
        handler.write(img_data)

save_image(get_image_url(book_url)[0], get_image_url(book_url)[1])