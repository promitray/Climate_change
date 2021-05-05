import requests
from datetime import datetime
import json

url = 'http://127.0.0.1:8080/Weather'

class DateTimeEncoder(json.JSONEncoder):
     def default(self, o):
         if isinstance(o, datetime):
             return o.isoformat()

         return json.JSONEncoder.default(self, o)

dt = json.loads(json.dumps(datetime(2021,4,25), cls=DateTimeEncoder))

body = {'dt': dt, 'AverageTemperature': 39.256, 'AverageTemperatureUncertainty': 0.37, 'City': 'Ahvaz', 'Country': 'Iran', 'Latitude': '31.35N', 'Longitude': '49.01E'}

print(body)

response = requests.post(url, json=body)
print (response.json(),len(response.json()))
