import requests
from bs4 import BeautifulSoup
import csv
import os

def get_all_categories():
    all_categories = {} ## need a dictionary to match the category to the category_number
    url = "http://books.toscrape.com/index.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser") ## parser type
    categories = soup.find("ul", {"class":"nav-list"}).find_all("a")

    for category in range(1, len(categories)):
        category_name = categories[category].get_text(strip=True).lower()
        all_categories[category_name] = "-".join(category_name.split(' ')) + '_' + str(category+1)

    return all_categories

print(get_all_categories().keys())
category = get_all_categories()[input("What book category do you want to scrape the data from: ").lower()]

def get_books_urls():
    url = "http://books.toscrape.com/catalogue/category/books/{0}".format(category)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser") 
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
    product_page_url = book_url
    universal_product_code = soup.find_all("td")[0].text
    title = soup.find("h1").text
    price_including_tax = ''.join(e for e in soup.find_all("td")[3].text if e.isnumeric() or e == "£" or e == ".") ## keeps only the price and currency
    price_excluding_tax = ''.join(e for e in soup.find_all("td")[2].text if e.isnumeric() or e == "£" or e == ".") ## keeps only the price and currency
    number_available = soup.find_all("td")[5].text
    product_description = soup.find("article", {"class":"product_page"}).find_all("p")[3].text
    category = soup.find("ul", {"class":"breadcrumb"}).find_all("a")[2].text
    review_rating = soup.find("p", {"class":"star-rating"})['class'][-1]
    image_url = "http://books.toscrape.com/" + soup.find("img")['src'].split('/',2)[-1]

    return product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url

def write_csv():
    print("Please wait...")
    en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]

    if not os.path.exists("./books-to-scrape"):
        os.makedirs("./books-to-scrape") ## creates the books folder 

    with open("./books-to-scrape/{0}_books.csv".format(''.join(category.split('_')[:-1])), "w", newline="") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=",") ## defines the writing method
        writer.writerow(en_tete) ## writes the columns title
        for book in get_books_urls(): ## writes the retrieved data in each column
            writer.writerow(get_book_infos(book))
    
    print("Scraping completed!")
    return

write_csv()
