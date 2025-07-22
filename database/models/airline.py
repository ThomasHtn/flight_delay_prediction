from sqlalchemy import Column, Integer, String

from database.base import Base


class Airline(Base):
    __tablename__ = "airlines"

    unique_carrier = Column(String, primary_key=True)
    airline_id = Column(Integer)
    carrier = Column(String)
