Instructions for usage:
##################################

Please clone this repo (https://github.com/promitray/Climate_change) and then navigate into the directory 'docker2': cd docker2

1. Bootstrap the DB
```bash
$ sudo docker-compose up -d db

$ sudo docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"
```

  mkdir data (docker2/data)  IMPORTANT: TO LOAD DATA INTO DATABASE, PLEASE COPY CSV FILE INTO THE this 'data' DIRECTORY: I have not yet been able to circumvent this step (yet).
  From directory 'docker2':
############################################################################################################################################################################
A. If local postgres service is running stop it
```bash
$ sudo service postgresql stop
```
B. Connect to postgres container
```bash
sudo docker exec -it docker2_db_1 bash
psql -U postgres
\l
\connect planetly_test
\dt
\d temp_data

COPY temp_data FROM '/data/GlobalLandTemperaturesByCity.csv' DELIMITER ',' CSV HEADER;

```
Exit postgres container
##############################################################################################################################################################################

2. Bring up the cluster
```bash
$ sudo docker-compose up -d
```

3. Please navigate to the examples directory and execute the python (.py) scripts to see the API (insert, update and getRecords endpoints) in action.

###########################################
Examples:

cd examples:

In the first query, we order by temperature (ASC/ DESC can be adjusted in the query) and then take the first occurence of every city. Some caution be exercised, same cities could (rarely) belong to two different countries.

a. GET reuqest with start date set to 1.1.2001 and end date unspecified (today taken as default), set LIMIT to 1. For input json structure, please see .py file for example 1. 

[{'dt': '2013-07-01T00:00:00', 'AverageTemperature': 39.156, 'AverageTemperatureUncertainty': 0.37, 'City': 'Ahvaz', 'Country': 'Iran', 'Latitude': '31.35N', 'Longitude': '49.01E'}] is the entry whose city has the highest AverageTemperature since the year 2000 corresponding to Ahvaz in Iran.

b. POST request using json response above and increase AverateTemperature by 0.1 (can be coded out continuously). Resulting json input is {'dt': dt, 'AverageTemperature': 39.256, 'AverageTemperatureUncertainty': 0.37, 'City': 'Ahvaz', 'Country': 'Iran', 'Latitude': '31.35N', 'Longitude': '49.01E'} with dt set to 25-4-2021 (random date last month) in datetime format. It can be verified that this entry is created. 

c. PUT request using json input as {'dt': dt, 'AverageTemperature': 37.256, 'City': 'Ahvaz'} with dt set to 25-4-2021 (random date last month referenced above) which updates above entry. Caution to be exercised while identifying rows with dt and city name. Some countries have same city names :) In this case, however, it works.

###############################################################
Time taken/ difficulties/ scope for improvement:

1. 3 hours of coding including references on how to containerize databases and flask applications using databases. Spent about 20 min after cross checking data from API response and actual CSV file.

2. Difficulties: I spent some time trying to make the data persist in the database but I am not able to do this at the moment (within the recommended time window) despite using volumes. The data gets lots once the containers are stopped and images are deleted. Other minor hassles included the data itself: some entries were identical but differed only in longitude, so I had to change the database structure (primary keys) and then continue.

3. Scope for improvement: I would really like to make the containerized database contain the data. Other improvement could include more elegant API end points (keeping REST principles intact) and fewer interdependecies. Alternatively, an AWS RDS could be used. Django would allow for a visual interface to the API which could be useful in adding, removing and modifying data. 


