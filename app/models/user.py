from sqlalchemy import Column, Integer, String
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    kakao_id = Column(Integer, primary_key=True, index=True, nullable=False)
    nickname = Column(String, nullable=False)
    profile_image = Column(String, unique=True, nullable=True)
