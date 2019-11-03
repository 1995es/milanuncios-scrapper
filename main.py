import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import re
from airtable import create_record, get_records
from constants import SELENIUM_DRIVERS_PATH

URL = 'https://www.milanuncios.com/entradas/granada-sound.htm?fromSearch=1&demanda=n'

# Configure the web driver
# Firefox
firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = True
browser = webdriver.Firefox(SELENIUM_DRIVERS_PATH, options=firefox_options)

# Chrome
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--enable-javascript")
# chrome_options.add_argument("--user-data-dir=seleniumchrome3")
# browser = webdriver.Chrome(SELENIUM_DRIVERS_PATH, options=chrome_options)

# Get and set implicit wait in case elements are not readily available
browser.get(URL)
browser.implicitly_wait(5)

# Get the saved items' list
records = get_records()

ad_list = browser.find_elements_by_class_name('aditem')
for ad_item in ad_list:
    try:
        id = ad_item.find_element_by_class_name('x5').text
    except NoSuchElementException as exception:
        print("ERROR: ID not found, skip!")
        id = None

    if id is None:
        continue

    # If the 'id' exists in the list, skip it 
    exists = False
    for record_id in records:
        if record_id == id:
            exists = True
            break

    if exists:
        continue

    try:
        ad = ad_item.find_element_by_class_name('aditem-detail')
    except NoSuchElementException as exception:
        print("ERROR: aditem-detail not found, skip!")
        continue

    try:
        item = ad.find_element_by_class_name('aditem-detail-title')
        title = item.text
        href = item.get_attribute('href')
    except NoSuchElementException as exception:
        title = None
        href = None

    try:
        desc = ad.find_element_by_class_name("tx").text
    except NoSuchElementException as exception:
        desc = None

    try:
        price = ad.find_element_by_class_name("aditem-price").text
    except NoSuchElementException as exception:
        price = None

    ad_content = {
        "id": id,
        "title": title,
        "description": desc,
        "url": href,
        "price": price
    }
    create_record(ad_content)

time.sleep(5)
browser.quit()
print("Bye!")
