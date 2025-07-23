from sqlalchemy import Column, Float, String, Integer

from database.base import Base


class Airport(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, unique=True, nullable=False)
    city_name = Column(String)
    state_abbr = Column(String)
    state_fips = Column(Float)
    state_name = Column(String)
    wac = Column(Float)
