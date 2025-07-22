from sqlalchemy.orm import Session

from database.base import SessionLocal
from database.models.airline import Airline
from database.models.airports import Airport
from database.models.flight import Flight


def get_all_flights(limit: int = 100):
    session: Session = SessionLocal()
    try:
        return session.query(Flight).limit(limit).all()
    finally:
        session.close()


def get_all_airports(limit: int = 100):
    session: Session = SessionLocal()
    try:
        return session.query(Airport).limit(limit).all()
    finally:
        session.close()


def get_all_airlines(limit: int = 100):
    session: Session = SessionLocal()
    try:
        return session.query(Airline).limit(limit).all()
    finally:
        session.close()
