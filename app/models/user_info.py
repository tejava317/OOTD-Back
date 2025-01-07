from sqlalchemy import Column, BigInteger, String, Text
from app.db.session import Base

class UserInfo(Base):
    __tablename__ = "user_info"
    
    kakao_id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    nickname = Column(String(30), nullable=False)
    profile_image = Column(Text, nullable=True)
