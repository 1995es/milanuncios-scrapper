# Milanuncios scrapper

Scrapping ads from Milanuncios and save them on Airtable. 
It uses Selenium for browser automation and Request library for saving the data throught Airtable API. 

## Getting started

### Airtable

Create an [Airtable account](https://airtable.com/invite/r/qWuaZmWg) if you don't have one.

1.  Open this example base: <https://airtable.com/shrdrxFgqF6teh1wf>
2.  Click on `Copy base` in the top right corner
3.  Click on your profile picture in the top right corner
4.  Select `Account`
5.  On the page click on `Generate API key` on the right side under API
    - This key is the `AIRTABLE_API_KEY`. Save it
6.  Go to the [API documentation page](https://airtable.com/api) and select the copied base
7.  Select `INTRODUCTION` on the left side. You should see something like this:  
    > The ID of this base is `apptA3435k56rI3cr`. 
    - Save it, it will be used as `AIRTABLE_BASE_ID`

### Environment variables

-   `AIRTABLE_API_KEY` - your account API key to access Airtable
-   `AIRTABLE_BASE_ID` - the ID of the Airtable base which is used to store the data
-   `AIRTABLE_BASE_TABLE` - the table to store the data in

1. Create a copy of `.env-example` and save it as `.env`
2. Write your keys `AIRTABLE_API_KEY` and `AIRTABLE_BASE_ID`. Leave `AIRTABLE_BASE_TABLE` as default.

### Install packages

Install the packets with `pip install -r requirements.txt`

## Usage

1. Change the `URL` variable on `main.py`
2. Run it with `python3 main.py`