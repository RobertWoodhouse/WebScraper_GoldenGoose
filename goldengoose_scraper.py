'''
Golden Goose Web Scraper
Author: Robert Woodhouse
Modified: 01/05/2023
'''

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas
import sqlite3
import json

'''
    "item_id":"GMF00102.F000311.10270",
    "item_name":"men’s super-star sneakers with suede star and blue heel tab",
    "price":390,
    "item_fullprice":390,
    "size":"",
    "quantity":"",
    "item_category":"men/sneakers/super-star",
    "available":true,
'''

product_dict = {"id": [],
                "name": [],
                "price": [],
                "description": [],
                "details": []}


driver = webdriver.Chrome('/Applications/WebDrivers/chromedriver')
driver.delete_all_cookies()

# TODO create URL builder
# Hardcoded URL
main_link = "https://www.goldengoose.com/gb/en/ls/men/sneakers"


def make_soup(url):
    driver.get(url)
    return BeautifulSoup(driver.page_source, "html.parser")


# Find all products on page
soup = make_soup(main_link)
product_grid = soup.find('ul', class_='row product-grid view-grid list-unstyled')
products = product_grid.find_all('li', class_='product-tile-container')
product_links = []

# Populate product_links array
for product in products:
    product_links.append(main_link + product.find('a').get('href'))
    #TODO remove break after scrapers have been built
    break

json_data = []

for link in product_links:
    soup = make_soup(link)
    product_wrapper = soup.find('div', class_='pdp__wrapper product-detail-page product-detail product-wrapper js-pdp-main')
    #product_data_json = product_wrapper.get('data-analytics')
    json_data.append(product_wrapper.get('data-analytics'))
    '''
    content_top = product_wrapper.find('div', class_='pdp__content--top')
    content_middle = product_wrapper.find('div', class_='pdp__content--middle')
    '''


# Connect to the SQLite database (creates the database if it doesn't exist)
conn = sqlite3.connect('gg_products.db')

# Create a cursor object
cursor = conn.cursor()

# Create the table
cursor.execute('''CREATE TABLE IF NOT EXISTS gg_table
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT)''')


# Insert the data into the table
for item in json_data:
    cursor.execute('''INSERT INTO gg_table (name)
        VALUES ( ?)
    ''', (item['name']))

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()


driver.close()
