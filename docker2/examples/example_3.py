import requests
from datetime import datetime
import json

url = 'http://127.0.0.1:8080/Weather'

class DateTimeEncoder(json.JSONEncoder):
     def default(self, o):
         if isinstance(o, datetime):
             return o.isoformat()

         return json.JSONEncoder.default(self, o)


dt = str(datetime(2021,4,25))

body = {'dt': dt, 'AverageTemperature': 37.256, 'City': 'Ahvaz'}

response = requests.put(url, json=body)
print (response.json(),len(response.json()))
