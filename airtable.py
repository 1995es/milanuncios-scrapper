import requests
from requests.adapters import HTTPAdapter
import json
import os
import posixpath

auth = "Bearer {}"


class Airtable(object):

    AIRTABLE_API_URL = "https://api.airtable.com/v0/"

    def __init__(self, base_id, table_name, api_key):
        self.table_url = posixpath.join(
            self.AIRTABLE_API_URL, base_id, table_name)
        self.api_key = api_key

    def create_payload(self, data):
        return {'fields': data}

    def create_record(self, data):
        """Create a new record with the params passed by arg

        Arguments:
            data -- pair key-value object

        Returns:
            boolean -- operation result
        """
        try:
            headers = {
                "Authorization": auth.format(self.api_key),
                "Content-Type": "application/json"
            }
            payload = json.dumps(self.create_payload(data))
            s = requests.Session()
            response = s.post(url=self.table_url, headers=headers,
                              data=payload, verify=True).json()
            if(len(response) > 0):
                if 'id' in response:
                    return True
                else:
                    return False
        except Exception as e:
            print(e)
            return False

    def get_records(self):
        """Return a list with the records's ID 

        Returns:
            array -- records' ID list
        """
        headers = {
            "Authorization": auth.format(self.api_key),
            "Content-Type": "application/json"
        }
        params = {'fields%5B%5D': 'id'}
        id_list = []
        offset = None
        while True:
            if(offset is not None):
                params.update({'offset': offset})
            response = requests.get(
                self.table_url, params=params, headers=headers).json()
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
                    break

        return id_list
