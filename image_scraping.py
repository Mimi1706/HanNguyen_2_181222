import requests
from bs4 import BeautifulSoup
import os ## to create a directory

book_url = "" ## paste the book link inside "" example: "http://books.toscrape.com/catalogue/the-cat-in-the-hat-beginner-books-b-1_235/index.html"

def get_book_infos(book_url):
    response = requests.get(book_url) ## gets to the book url
    soup = BeautifulSoup(response.text, "html.parser") 

    ## retrieves the following data:
    title = '_'.join(e for e in soup.find("h1").text.lower().split(' ') if e.isalnum()) ## filters all the special characters to avoid errors when saving the image name
    image_url = "http://books.toscrape.com/" + soup.find("img")['src'].split('/',2)[-1]

    return title,image_url

def get_image(title,image_url):
    if not os.path.exists("./images"):
        os.makedirs("./images") ## creates the books folder

    img_data = requests.get(image_url).content ## retrieves the image content via the url
    with open('./images/{0}.jpg'.format(title), 'wb') as image_file:
        image_file.write(img_data) ## saves the image

    return

get_image(get_book_infos(book_url)[0], get_book_infos(book_url)[1])