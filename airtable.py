import requests
from requests.adapters import HTTPAdapter
import json
import os
from constants import AIRTABLE_URL, AIRTABLE_API_KEY

auth = "Bearer {}"
headers = {
    "Authorization": auth.format(AIRTABLE_API_KEY),
    "Content-Type": "application/json"
}


def create_payload(data):
    return {'fields': data}


def create_record(data):
    """Create a new record with the params passed by arg

    Arguments:
        data -- pair key-value object

    Returns:
        boolean -- operation result
    """
    payload = json.dumps(create_payload(data))
    s = requests.Session()
    response = s.post(url=AIRTABLE_URL, headers=headers,
                      data=payload, verify=True).json()
    if(len(response) > 0):
        if 'id' in response:
            return True
        else:
            return False


def get_records():
    """Return a list with the records's ID 

    Returns:
        array -- records' ID list
    """
    params = {'fields%5B%5D': 'id'}
    id_list = []
    offset = None
    while True:
        if(offset is not None):
            params.update({'offset': offset})
        response = requests.get(
            AIRTABLE_URL, params=params, headers=headers).json()
        if(len(response) > 0):
            if 'records' in response:
                for item in response['records']:
                    id_list.append(item['fields']['id'])
                if 'offset' in response:
                    offset = response['offset']
                else:
                    break
            if 'error' in response:
                err = response['error']

    return id_list
