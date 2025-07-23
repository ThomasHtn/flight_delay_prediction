from sqlalchemy import Column, Integer, String

from database.base import Base


class Airline(Base):
    __tablename__ = "airlines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    unique_carrier = Column(String, unique=True, nullable=False)
    airline_id = Column(Integer)
    carrier = Column(String)
