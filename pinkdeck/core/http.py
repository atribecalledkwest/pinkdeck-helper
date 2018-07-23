import requests
from pinkdeck.core import config

VALID_METHODS = [
    "get",
    "post",
    "put",
    "head",
    "options"
]

class HttpApiError(Exception):
    pass

def send_http_request(info):
    method = info.get("method")
    url = info.get("url")
    data = info.get("data")

    if method.lower() not in VALID_METHODS:
        raise HttpApiError("Invalid method given")

    headers = {
        "User-Agent": config.USER_AGENT
    }

    func = getattr(requests, method.lower())

    req = func(url, data=data, headers=headers)

    if req.status_code != 200:
        raise HttpApiError(req.text)
