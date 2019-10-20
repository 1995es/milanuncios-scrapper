import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import re
from airtable import create_record, get_records

# Optional argument, if not specified will search path.
opts = Options()
opts.set_headless = True

URL = 'https://www.milanuncios.com/entradas/granada-sound.htm?fromSearch=1&demanda=n'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--enable-javascript")
chrome_options.add_argument("--user-data-dir=seleniumchrome3") 
driver = webdriver.Firefox('/Users/marcosandreo/workspace/python/selenium-drivers', options=opts)
#driver = webdriver.Chrome('/Users/marcosandreo/workspace/python/selenium-drivers/chromedriver', options=chrome_options) 
driver.get(URL)

# Set implicit wait in case elements are not readily available
driver.implicitly_wait(5)

# Download the actual items
items = get_records()

#time.sleep(5)  # Let the user actually see something!

aditem_list = driver.find_elements_by_class_name('aditem') 
for aditem in aditem_list:
    #print(ad.text)
    try:
        id = aditem.find_element_by_class_name('x5').text
    except Exception:
        id = None

    if(id is None):
        continue

    # Look for the ID in the downloaded ID list
    # If already exists, skip it
    exist = False
    for it in items:
        if it == id:
            exist = True
            break

    if(exist):
        continue
        
    try:
        ad = aditem.find_element_by_class_name('aditem-detail') 
    except Exception:
        continue
   
    title = None
    href = None
    try:
        item = ad.find_element_by_class_name('aditem-detail-title')
        title = item.text
        href = item.get_attribute('href')
    except Exception:
        print(Exception)
        
    try:
        desc = ad.find_element_by_class_name("tx").text
    except Exception:
        desc = None
    try:
        price = ad.find_element_by_class_name("aditem-price")
        price = price.text
    except Exception:
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
driver.quit()
print("Bye!")
