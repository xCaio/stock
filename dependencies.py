from sqlalchemy.orm import sessionmaker
from database import engine


def get_session():
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
