from sqlalchemy import Column, Integer, String, Date
from app.db.session import Base

class Weather(Base):
    __tablename__ = "weather"
    
    weather_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    location = Column(String(60), nullable=False)
