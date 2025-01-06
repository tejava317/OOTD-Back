from sqlalchemy import Column, Integer, String
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    kakao_id = Column(Integer, unique=True, index=True, nullable=False)
    nickname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
