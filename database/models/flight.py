from sqlalchemy import Column, Float, Integer, String

from database.base import Base


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Date information
    year = Column(Integer)
    quarter = Column(Integer)
    month = Column(Integer)
    day_of_month = Column(Integer)
    day_of_week = Column(Integer)

    # Airline information
    unique_carrier = Column(String)

    # Origin airport
    origin = Column(String)
    origin_state_abr = Column(String)
    origin_state_fips = Column(Float)
    origin_wac = Column(Float)

    # Destination airport
    dest = Column(String)
    dest_state_abr = Column(String)
    dest_state_fips = Column(Float)
    dest_wac = Column(Float)

    # Schedule and time details
    crs_dep_time = Column(Float)
    dep_time_blk = Column(String)
    taxi_out = Column(Float)
    taxi_in = Column(Float)
    crs_arr_time = Column(Float)
    crs_elapsed_time = Column(Float)

    # Delay target
    arr_del15 = Column(Float)

    # Distance information
    distance = Column(Float)
    distance_group = Column(Float)
