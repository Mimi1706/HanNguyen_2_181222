[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

## [OpenClassrooms] - Projet 2 : Utiliser les bases de Python pour l'analyse de marché

As part of the Openclassrooms [Python software developer program](https://openclassrooms.com/fr/paths/518-developpeur-dapplication-python), this project introduces to the basics of Python by setting up a pipeline ETL with Requests and BeautifulSoup.

The goals were to create several scripts to:

- scrape the requested data (title, description, price, UPC...) and cover of one book
- scrape the requested data (title, description, price, UPC...) of all the books for each category
- scrape the books cover and sort them by category

### Books Online

Books Online is an online library platform looking to set up a price monitoring system. Their first goal is to elaborate a static solution to retrieve all the necessary data from a website called [Books to scrape](http://books.toscrape.com).

## Prerequisites for installation

- [Python3](https://www.python.org/downloads/)
- Pip3 (If Python3 is installed, you can install pip3 with `python -m pip3 install`)

### Dependencies

The dependencies and their versions are listed in the `requirements.txt` but mainly, it requires:

- BeautifulSoup
- Requests

## Installing and lauching

1. Clone or download the content of [this repository](https://github.com/Mimi1706/HanNguyen_2_181222)
2. (⚠️ Please make sure you're in the right directory for the next steps)
3. Create your environment with `Python3 -m venv env` (the recommended name is env)
4. Activate your environement with `source env/bin/activate`
5. Install the dependencies for your environment with `pip3 install -r requirements.txt`
6. Launch the script you want in your terminal, the title of each script is self-explanatory, for example type: `all_books_scraping.py` will scrape all the books, then follow the terminal instructions.

## Script description

- **all_books_scraping**: will scrape the entirety of the books infos in one unique CSV file
- **all_categories_books_scraping**: will scrape the entirety of the books info in several CSV files by categories
- **all_categories_images_scraping**: will scrape the entirety of the books cover in several folders by categories
- **category_books_scraping**: will scrape the chosen book category by the user in the terminal
- **category_images_scraping**: will scrape the covers from the chosen book category by the user in the terminal
- **one_book_scraping**: will scrape one book infos and cover from the URL pasted in the terminal by the user
