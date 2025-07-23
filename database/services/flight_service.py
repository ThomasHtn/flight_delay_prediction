import pandas as pd
from loguru import logger
from sklearn.model_selection import train_test_split
from sqlalchemy.orm import Session

from database.base import SessionLocal, engine
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


def load_training_data() -> pd.DataFrame:
    """Load a stratified 20% sample of training data from flights, airlines, and airports."""
    logger.info("Loading training data from database...")

    query = """
    SELECT
        flights.month,
        flights.day_of_week,
        flights.crs_dep_time,
        flights.crs_arr_time,
        flights.crs_elapsed_time,
        flights.distance,
        airlines.unique_carrier,
        airports_origin.code AS origin,
        airports_dest.code AS dest,
        flights.dep_time_blk,
        flights.arr_del15
    FROM flights
    JOIN airlines ON airlines.id = flights.airline_id
    JOIN airports AS airports_origin ON airports_origin.id = flights.origin_id
    JOIN airports AS airports_dest ON airports_dest.id = flights.dest_id
    WHERE arr_del15 IS NOT NULL
    """

    df = pd.read_sql(query, engine)

    if df.empty:
        logger.warning("No training data found.")
        return df

    df = df.dropna()
    logger.success(f"{len(df)} total rows loaded before sampling.")

    # Stratified sampling: keep 20% while preserving class distribution
    _, df_sampled = train_test_split(
        df, test_size=0.2, stratify=df["arr_del15"], random_state=42
    )

    logger.success(f"{len(df_sampled)} rows returned after 20% stratified sampling.")
    return df_sampled.reset_index(drop=True)
