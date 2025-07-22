from typing import Optional

from pydantic import BaseModel


class FlightBase(BaseModel):
    # Date information
    year: int
    quarter: int
    month: int
    day_of_month: int
    day_of_week: int

    # Airline information
    unique_carrier: str

    # Origin airport
    origin: str
    origin_state_abr: str
    origin_state_fips: Optional[float]
    origin_wac: Optional[float]

    # Destination airport
    dest: str
    dest_state_abr: str
    dest_state_fips: Optional[float]
    dest_wac: Optional[float]

    # Schedule and time details
    crs_dep_time: Optional[float]
    dep_time_blk: str
    taxi_out: Optional[float]
    taxi_in: Optional[float]
    crs_arr_time: Optional[float]
    crs_elapsed_time: Optional[float]

    # Delay target
    arr_del15: Optional[float]

    # Distance information
    distance: Optional[float]
    distance_group: Optional[float]


class FlightCreate(FlightBase):
    pass  # for creation use-case, identical to base


class FlightRead(FlightBase):
    id: int

    class Config:
        orm_mode = True
