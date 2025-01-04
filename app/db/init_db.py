from app.db.session import engine, Base
from app.models import users, weather

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()