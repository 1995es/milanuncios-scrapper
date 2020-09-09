import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import re
from environs import Env
from airtable import Airtable
from datetime import timedelta, datetime

URL = 'https://www.milanuncios.com/entradas/granada-sound.htm?fromSearch=1&demanda=n'

# Handle environment variables
env = Env()
env.read_env()

# Configure the web driver
# Firefox
firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = True
browser = webdriver.Firefox(
    env('SELENIUM_DRIVERS_PATH'), options=firefox_options)

# Chrome
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--enable-javascript")
# chrome_options.add_argument("--user-data-dir=seleniumchrome3")
# browser = webdriver.Chrome(SELENIUM_DRIVERS_PATH, options=chrome_options)

# Get the saved items' list
airtable = Airtable(env("AIRTABLE_BASE_ID"), env(
    "AIRTABLE_BASE_TABLE"), env("AIRTABLE_API_KEY"))
records = airtable.get_records()

# Get and set implicit wait in case elements are not readily available
browser.get(URL)
browser.implicitly_wait(5)

page = 1
while True:
    ad_list = browser.find_elements_by_class_name('aditem')
    for ad_item in ad_list:
        try:
            id = ad_item.find_element_by_class_name('x5').text
        except NoSuchElementException as exception:
            print("ERROR: ID not found, skip!")
            id = None

        if id is None:
            continue

        try:
            date = ad_item.find_element_by_class_name('x6').text
        except NoSuchElementException as exception:
            date = None

        current_date_and_time = datetime.now()
        try:
            if('horas' in date):
                hours = date.split(' ')[0]
                hours_delta = timedelta(hours=int(hours))
                correct_date_and_time = current_date_and_time - hours_delta
            elif ('días' in date):
                days = date.split(' ')[0]
                days_delta = timedelta(days=int(days))
                correct_date_and_time = current_date_and_time - days_delta
            else:
                correct_date_and_time = current_date_and_time
        except:
            correct_date_and_time = current_date_and_time

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
            price = float(price[0:-1].replace('.', ''))
        except NoSuchElementException as exception:
            price = None

        ad_content = {
            "id": id,
            "title": title,
            "description": desc,
            "url": href,
            "price": price,
            "publish_date": correct_date_and_time.strftime("%Y-%m-%d")
        }
        airtable.create_record(ad_content)

    # Go to the next page
    last_page = False
    while True:
        try:
            browser.implicitly_wait(20)
            continue_link = browser.find_element_by_xpath(
                "//a[contains(text(), 'Siguiente')]")
            continue_link.click()
            time.sleep(5)
            page += 1
            print('>>>> go to page', page)
            break
        except NoSuchElementException as exception:
            last_page = True
            break
        except ElementClickInterceptedException as exception:
            print(exception)
            print('try again')

    if(last_page):
        break

browser.quit()
print("Good Bye!")
