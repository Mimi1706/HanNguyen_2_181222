import requests
from bs4 import BeautifulSoup
import csv
import os

book_url = "" ## paste the book link inside "" example: "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

def get_book_infos(book_url):
    response = requests.get(book_url) ## gets to the book url
    soup = BeautifulSoup(response.text, "html.parser") 

    ## retrieves the following data
    product_page_url = book_url
    universal_product_code = soup.find_all("td")[0].text
    title = ' '.join(e for e in soup.find("h1").text.lower().split(' ') if e.isalnum())
    price_including_tax = soup.find_all("td")[3].text
    price_excluding_tax = soup.find_all("td")[2].text
    number_available = soup.find_all("td")[5].text
    product_description = soup.find("article", {"class":"product_page"}).find_all("p")[3].text
    category = soup.find("ul", {"class":"breadcrumb"}).find_all("a")[2].text
    review_rating = soup.find("p", {"class":"star-rating"})['class'][-1]
    image_url = "http://books.toscrape.com/" + soup.find("img")['src'].split('/',2)[-1]

    ##.lower().split(' ') if e.isalnum())

    return product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url

def get_book():
    en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]

    book_title = '_'.join(get_book_infos(book_url)[2].split(' '))

    if not os.path.exists("./{0}".format(book_title)):
        os.makedirs("./{0}".format(book_title)) ## creates the category folder

    with open("{0}/{0}.csv".format(book_title), "w", newline="") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=",") ## defines the writing method
        writer.writerow(en_tete) ## writes the columns title
        writer.writerow(get_book_infos(book_url))
    
    img_data = requests.get(get_book_infos(book_url)[-1]).content ## retrieves the image content via the url
    with open('./{0}/{0}.jpg'.format(book_title), 'wb') as image_file:
        image_file.write(img_data) ## saves the image
    
get_book()
