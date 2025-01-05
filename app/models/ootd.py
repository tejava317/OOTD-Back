from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.session import Base

class OOTD(Base):
    __tablename__ = "ootd"
    
    ootd_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    weather_id = Column(Integer, ForeignKey("weather.weather_id"), nullable=False)
    photo_url = Column(String, nullable=False)
