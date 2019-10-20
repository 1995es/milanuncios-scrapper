import requests
from requests.adapters import HTTPAdapter
import json
import os
from dotenv import load_dotenv
from constants import URL

load_dotenv()

auth = "Bearer {}"
headers = {
    "Authorization": auth.format(os.getenv('AIRTABLE_API_KEY')),
    "Content-Type": "application/json"
}


def create_payload(data):
    return {'fields': data}


def create_record(data):
    payload = create_payload(data)
    payload = json.dumps(payload)
    s = requests.Session()
    r = s.post(url=URL, headers=headers, data=payload, verify=True)
    res = r.json()
    #print(res)


def get_records():
    url_list = URL + "?fields%5B%5D=id"
    r = requests.get(url_list, headers=headers)
    data = r.json()
    items = []
    if(len(data) > 0):
        for item in data["records"]:
            items.append(item["fields"]["id"])
    return items

