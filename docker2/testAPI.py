import requests
from datetime import datetime

import json


#url = 'http://127.0.0.1:5000/Weather?City=Pune&start_date=2021-04-28&end_date=2021-05-02'

url = 'http://127.0.0.1:8080/Weather'

# # #get request
body = {
 	'start_date':str(datetime(2000, 1, 1)),
 	'end_date':str(datetime(2021, 5, 3)),
        'limit_number': 1
 }


response = requests.get(url, params = body)
res=response.json()
print (json.loads(res['result']))


#insert request



# class DateTimeEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, datetime):
#             return o.isoformat()

#         return json.JSONEncoder.default(self, o)

# # dt = json.loads(json.dumps(datetime.now(), cls=DateTimeEncoder))
# dt = json.loads(json.dumps(datetime(2021,3,29), cls=DateTimeEncoder))

# body = {'dt' : dt,
#         'AverageTemperature' : 32.6,
#         'AverageTemperatureUncertainty' : 2.8,
#         'City' : 'Pune',
#         'Country' : 'India',
#         'Latitude' : '18.5204° N',
#         'Longitude' : '73.8567° E'
#         }        
# #print(body)

# response = requests.post(url, json=body)
# print (response.json(),len(response.json()))


# Update request
# dt = str(datetime(2021,4,28,18,39,28,195422))
# dt = str(datetime(2021,4,28))
# body = {'dt' : dt,
#         'AverageTemperature' : 23.2,
#         'AverageTemperatureUncertainty' : 6.8,
#         'City' : 'Pune',
#         }       
# response = requests.put(url, json=body)
# print (response.json(),len(response.json()))
