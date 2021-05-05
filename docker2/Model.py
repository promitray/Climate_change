from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from database import Base


class temp_data(Base):
    __tablename__ = 'temp_data'
    # id = Column(Integer, primary_key=True)
#     dt = Column(String)
    dt = Column(DateTime, primary_key=True)
    AverageTemperature = Column(Float)
    AverageTemperatureUncertainty = Column(Float)
    City = Column(String, primary_key=True)
    Country = Column(String, primary_key=True)
    Latitude = Column(String, primary_key=True)
    Longitude = Column(String, primary_key=True)
    
    def __repr__(self):
        return "<temp_data(city='{}', AverageTempetarue='{}', AverageTemperatureUncertainty={}, dt={})>"\
                .format(self.City, self.AverageTemperature, self.AverageTemperatureUncertainty, self.dt)   
