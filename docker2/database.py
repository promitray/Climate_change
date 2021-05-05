from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import and_,create_engine
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime
import pandas as pd
import traceback
import json
import os

engine = create_engine('postgresql://postgres:postgres@db:5432/planetly_test') 
# engine = create_engine('postgresql://user1:12345@db:5432/planetly_test') 
# engine = create_engine('postgresql://user1:12345@localhost:5432/planetly_test') #Use this for local/non docker database connection

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import Model
    Base.metadata.create_all(bind=engine)

def recreate_database():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import Model
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)


Session = sessionmaker(bind=engine)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

from Model import  temp_data

def insertRecord(jsonData):
    try:
        s = Session()
        jsonData['dt'] = datetime.fromisoformat(jsonData['dt'])
        r = s.query(temp_data).filter_by(City=jsonData['City'],dt=jsonData['dt']).first()
        if r:
            print("Record already exists, are you looking to update instead?")
            status = 401
            return status
        record = temp_data(**jsonData)
        print("Insert Successfull")
        s.add(record)
        s.commit()
        status = 200
    except Exception as e:
        print("Failed to insert record into table", e)
        traceback.print_exc()
        status = 400
    finally:
        if (s):
            s.close()
            print("The connection is closed")
        return status

def updateRecord(jsonData):
    try:
        s = Session()
        updateData = {}
        if 'AverageTemperature' in jsonData:
            updateData[temp_data.AverageTemperature] = jsonData['AverageTemperature']
        if 'AverageTemperatureUncertainty' in jsonData:
            updateData[temp_data.AverageTemperatureUncertainty] = jsonData['AverageTemperatureUncertainty']
        r = s.query(temp_data).filter(temp_data.City==jsonData['City'],temp_data.dt==jsonData['dt'])
        r.update(updateData)
        s.commit()
        print("Update successfull")   
        status = 200     
    except Exception as e:
        print("Failed to insert record into table", e)
        traceback.print_exc()
        status = 400
    finally:
        if (s):
            s.close()
            print("The connection is closed")
        return status

def getRecords(jsonData):
    try:
        start_date = datetime.fromisoformat(jsonData['start_date'])
        end_date = datetime.fromisoformat(jsonData['end_date'])
        limit_number =  jsonData['limit_number']
        #city = jsonData['City']

        query = """
                    WITH derived_query AS
                   (SELECT * FROM
                   (SELECT *, ROW_NUMBER() OVER 
                   (PARTITION BY ("City") ORDER BY "AverageTemperature" DESC) rn
                    FROM temp_data
                    WHERE "dt" >= '"""+str(start_date)+"""' AND "dt" <= '"""+str(end_date)+""""' and "AverageTemperature" IS NOT NULL
                    ) tmp WHERE rn = 1)
                    SELECT * FROM derived_query 
                    ORDER BY "AverageTemperature" DESC LIMIT '"""+str(limit_number)+"""'

                """

        df1 = pd.read_sql_query(query, con=engine)
        del df1['rn']
        result = df1.to_dict(orient='record')
        result = json.dumps(result, cls = DateTimeEncoder)
        status = 200     
    except Exception as e:
        print("Failed to insert record into table", e)
        traceback.print_exc()
        status = 400
    finally:
        return status,result
