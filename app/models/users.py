from sqlalchemy import Column, Integer, String
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String, unique=True, index=True)
    nickname = Column(String, nullable=False)
