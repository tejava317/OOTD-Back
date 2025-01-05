from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from app.db.session import Base

class OOTD(Base):
    __tablename__ = "ootd"
    
    ootd_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    weather_id = Column(Integer, ForeignKey("weather.weather_id"), nullable=False)
    photo_url = Column(String, nullable=False)
    satisfaction_score = Column(Integer, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "satisfaction_score BETWEEN 1 AND 5 OR satisfaction_score IS NULL",
            name="check_satisfaction_score_range"
        ),
    )
