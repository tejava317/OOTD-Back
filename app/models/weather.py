from sqlalchemy import Column, Integer, String, Date
from app.db.session import Base

class Weather(Base):
    __tablename__ = "weather"
    
    weather_id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)
    date = Column(Date, nullable=False)
