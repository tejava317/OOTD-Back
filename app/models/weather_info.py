from sqlalchemy import Column, Integer, Float, ForeignKey
from app.db.session import Base

class WeatherInfo(Base):
    __tablename__ = "weather_info"

    weather_id = Column(Integer, ForeignKey("weather.weather_id"), primary_key=True)
    actual_temp = Column(Float, nullable=False)
    apparent_temp = Column(Float, nullable=False)
    precipitation = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)
    wind_speed = Column(Float, nullable=False)
    condition = Column(str, nullable=False)
    temp_6am = Column(Float, nullable=False)
    temp_12pm = Column(Float, nullable=False)
    temp_6pm = Column(Float, nullable=False)
    temp_12am = Column(Float, nullable=False)
