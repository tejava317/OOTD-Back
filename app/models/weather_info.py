from sqlalchemy import Column, Integer, Float, String, ForeignKey, CheckConstraint
from app.db.session import Base

class WeatherInfo(Base):
    __tablename__ = "weather_info"

    weather_id = Column(Integer, ForeignKey("weather.weather_id", ondelete="CASCADE"), primary_key=True)
    actual_temp = Column(Float, nullable=False)
    apparent_temp = Column(Float, nullable=False)
    precipitation = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)
    wind_speed = Column(Float, nullable=False)
    condition = Column(String(20), nullable=False)
    temp_6am = Column(Float, nullable=False)
    temp_12pm = Column(Float, nullable=False)
    temp_6pm = Column(Float, nullable=False)
    temp_12am = Column(Float, nullable=False)
