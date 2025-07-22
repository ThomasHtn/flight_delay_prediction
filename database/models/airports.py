from sqlalchemy import Column, Float, String

from database.base import Base


class Airport(Base):
    __tablename__ = "airports"

    code = Column(String, primary_key=True)
    city_name = Column(String)
    state_abbr = Column(String)
    state_fips = Column(Float)
    state_name = Column(String)
    wac = Column(Float)
