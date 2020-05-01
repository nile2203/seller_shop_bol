import requests


class BolooAccessor:
    def __init__(self):
        self.url = None
        self.method = None
        self.token = None
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    def set_url(self, url):
        self.url = url
        return self

    def set_method(self, method):
        self.method = method
        return self

    def make_request(self, data=None):
        if not self.method:
            return 0, 'No method set for the request', None

        if not self.url:
            return 0, 'No URL provided for the request', None

        if self.method == 'POST':
            response = requests.post(url=self.url, data=data, headers=self.headers)
            status_code = response.status_code
            if status_code == 200:
                return 1, 'Request successful', response.content

            if status_code == 500:
                return 0, 'Unable to reach bol server right now. Try again', None

            if status_code == 400:
                return 0, response.content, None

        return 0, 'Invalid method', None

    def get_access_token(
            self,
            client_id,
            client_secret):
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
        }

        return self.set_url('https://login.bol.com/token').set_method('POST').make_request(data=data)
