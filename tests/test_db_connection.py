from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.db.session import engine, SessionLocal

def test_connection():
    try:
        with engine.connect() as connection:
            print("Database connected successfully")
        
        session = SessionLocal()

        query = text("SELECT * FROM users")
        result = session.execute(query).fetchall()

        for row in result:
            print(f"user_id: {row.user_id}, nickname: {row.nickname}, email: {row.google_id}")

        session.close()
    except Exception as e:
        print("Database connection failed")
        print(e)

if __name__ == "__main__":
    test_connection()
