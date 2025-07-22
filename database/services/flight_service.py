from sqlalchemy.orm import Session

from database.base import SessionLocal
from database.models.flight import Flight


def get_all_flights(limit: int = 100):
    session: Session = SessionLocal()
    try:
        return session.query(Flight).limit(limit).all()
    finally:
        session.close()
