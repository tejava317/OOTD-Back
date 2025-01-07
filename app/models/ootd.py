from sqlalchemy import Column, Integer, BigInteger, Text, ForeignKey, CheckConstraint
from app.db.session import Base

class OOTD(Base):
    __tablename__ = "ootd"
    
    ootd_id = Column(Integer, primary_key=True, autoincrement=True)
    kakao_id = Column(BigInteger, ForeignKey("user_info.kakao_id", ondelete="CASCADE"), nullable=False)
    weather_id = Column(Integer, ForeignKey("weather.weather_id", ondelete="CASCADE"), nullable=False)
    photo_url = Column(Text, nullable=False)
    satisfaction_score = Column(Integer, nullable=True, default=None)
    
    __table_args__ = (
        CheckConstraint(
            "satisfaction_score BETWEEN 1 AND 5 OR satisfaction_score IS NULL",
            name="check_satisfaction_score_range"
        ),
    )
