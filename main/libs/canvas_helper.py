import requests
import json
from urllib.parse import urlparse, parse_qs


class JsonResponse:
    pass


class HttpCanvasAuthorizedRequest:
    def __init__(self, options, end_point, query):
        self.end_point = end_point
        self.bearer_token = f"Bearer {options.get('token')}"
        self.url = options.get("canvas_url")
        self.query = query

    def send_request(self):
        url = f"{self.url}{self.end_point}"
        headers = {'Authorization': self.bearer_token}
        response = requests.get(url, headers=headers, params=self.query)

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return None
