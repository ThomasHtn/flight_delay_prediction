from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String

from database.base import Base


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, autoincrement=True)

    year = Column(Integer)
    quarter = Column(Integer)
    month = Column(Integer)
    day_of_month = Column(Integer)
    day_of_week = Column(Integer)
    fl_date = Column(Date)

    unique_carrier = Column(String, ForeignKey("airlines.unique_carrier"))
    flight_num = Column(String)
    tail_num = Column(String)

    origin = Column(String, ForeignKey("airports.code"))
    dest = Column(String, ForeignKey("airports.code"))

    crs_dep_time = Column(Float)
    dep_time_blk = Column(String)
    taxi_out = Column(Float)
    taxi_in = Column(Float)
    crs_arr_time = Column(Float)
    arr_del15 = Column(Float)
    crs_elapsed_time = Column(Float)
    distance = Column(Float)
    distance_group = Column(Float)
    carrier_delay = Column(Float)
    weather_delay = Column(Float)
    nas_delay = Column(Float)
    security_delay = Column(Float)
    late_aircraft_delay = Column(Float)
    first_dep_time = Column(Float)
    total_add_gtime = Column(Float)
    longest_add_gtime = Column(Float)

    cancelled = Column(Boolean)
    cancellation_code = Column(String)
    diverted = Column(Boolean)
