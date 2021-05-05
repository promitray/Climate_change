import requests
from datetime import datetime
import json


url = 'http://127.0.0.1:8080/Weather'

body = {
 	'start_date':str(datetime(2000, 1, 1)),
 	'limit_number': 1
 }


response = requests.get(url, params = body)
res=response.json()
print (json.loads(res['result']))
