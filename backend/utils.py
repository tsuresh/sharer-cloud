from asyncio.windows_events import NULL
import json
import requests
from types import SimpleNamespace

baseEndpoint = "http://localhost:5000/"

def makeRestCall(endPoint, body):
    url = baseEndpoint + endPoint
    payload = json.dumps(body)
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code in [200, 201]:
        #print(response.text)
        return json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))
    else:
        return NULL