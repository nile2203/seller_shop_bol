import json
import requests


class BolooAccessor:
    def __init__(self, access_token=None):
        self.url = None
        self.method = None
        self.token = None
        self.access_token = access_token
        self.headers = {
            'Accept': 'application/json'
        }
        self.api_base_url = 'https://api.bol.com/'

    def set_url(self, url):
        self.url = url
        return self

    def set_method(self, method):
        self.method = method
        return self

    def set_headers(self, key, value):
        self.headers[key] = value
        return self

    def make_request(self, data=None):
        if not self.method:
            return 0, 'No method set for the request', None

        if not self.url:
            return 0, 'No URL provided for the request', None

        if self.method == 'POST':
            response = requests.post(url=self.url, data=data, headers=self.headers)
        elif self.method == 'GET':
            response = requests.get(url=self.url, headers=self.headers)
        else:
            return 0, 'Invalid method', None

        print(response.headers, response.content, response.status_code)
        status_code = response.status_code
        if status_code == 200:
            return 1, 'Request successful', json.loads(response.content.decode('utf-8'))

        if status_code == 500:
            return 0, 'Unable to reach bol server right now. Try again', None

        if status_code == 400:
            return 0, json.loads(response.content.decode('utf-8')), None

        if status_code == 401:
            return -1, json.loads(response.content.decode('utf-8')), None

        if status_code == 429:
            return -2, 'Too many requests', None

    def get_access_token(self, client_id, client_secret):
        if not (client_id and client_secret):
            return 0, 'Client credentials not provided', None

        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
        }
        self.set_url('https://login.bol.com/token').set_method('POST').set_headers(
            key='Content-Type', value='application/x-www-form-urlencoded')

        return self.make_request(data=data)

    def get_all_shipments(self, page_number, fulfilment_method):
        if not self.access_token:
            return 0, 'Access token not provided', None

        self.set_url('{}retailer/shipments/?page={}&fulfilment-method={}'.format(
            self.api_base_url, page_number, fulfilment_method)).set_method('GET').set_headers(
            key='Accept', value='application/vnd.retailer.v3+json').set_headers(
            key='Authorization', value='Bearer {}'.format(self.access_token))

        return self.make_request()

    def get_shipment_details(self, shipment_id):
        if not self.access_token:
            return 0, 'Access token not provided', None

        if not shipment_id:
            return 0, 'Shipment ID not provided', None

        self.set_url('{}retailer/shipments/{}'.format(self.api_base_url, shipment_id)).set_method('GET').set_headers(
            key='Accept', value='application/vnd.retailer.v3+json').set_headers(
            key='Authorization', value='Bearer {}'.format(self.access_token))

        return self.make_request()


