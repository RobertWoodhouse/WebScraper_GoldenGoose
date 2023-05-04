'''
Golden Goose Web Scraper
Author: Robert Woodhouse
Modified: 04/05/2023
'''

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas
import sqlite3
import json

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
    # TODO remove break after scrapers have been built
    break

json_data = []

for link in product_links:
    soup = make_soup(link)
    product_wrapper = soup.find('div', class_='pdp__wrapper product-detail-page product-detail product-wrapper js-pdp-main')
    json_data.append(product_wrapper.get('data-analytics'))

    # TODO Scrape description data from content_middle
    '''
    content_top = product_wrapper.find('div', class_='pdp__content--top')
    content_middle = product_wrapper.find('div', class_='pdp__content--middle')
    '''

# Example of data in json file
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

# TODO populate sqlite database
conn = sqlite3.connect('gg_products.db')
cursor = conn.cursor()

# Close the cursor, connection and driver
cursor.close()
conn.close()
driver.close()
