from pydantic import BaseModel


class FlightFeatures(BaseModel):
    month: int
    day_of_week: int
    crs_dep_time: int
    crs_arr_time: int
    crs_elapsed_time: int
    distance: float
    unique_carrier: str
    origin: str
    dest: str
    dep_time_blk: str
