import requests


class HttpClient:

    def __init__(self, timeout=30):
        self.timeout = timeout

    def get(self, url, params=None, headers=None):

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=self.timeout
        )

        response.raise_for_status()

        return response

    def post(self, url, data=None, json=None, headers=None):

        response = requests.post(
            url,
            data=data,
            json=json,
            headers=headers,
            timeout=self.timeout
        )

        response.raise_for_status()

        return response