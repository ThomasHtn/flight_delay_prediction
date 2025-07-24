from collections import Counter

import pandas as pd
from loguru import logger
from sklearn.model_selection import train_test_split
from sqlalchemy import select
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


def get_airport_code_to_id() -> dict:
    with SessionLocal() as session:
        return {
            airport.code: airport.id
            for airport in session.execute(select(Airport)).scalars()
        }


def get_airline_code_to_id() -> dict:
    with SessionLocal() as session:
        return {
            airline.unique_carrier: airline.id
            for airline in session.execute(select(Airline)).scalars()
        }


def load_training_data() -> pd.DataFrame:
    """Load a stratified 20% sample of training data from flights, airlines, and airports."""
    logger.info("Loading training data from database...")

    # Query with id to improve performance
    # query = """
    # SELECT
    #     flights.month,
    #     flights.day_of_week,
    #     flights.crs_dep_time,
    #     flights.crs_arr_time,
    #     flights.crs_elapsed_time,
    #     flights.distance,
    #     flights.airline_id,
    #     flights.origin_id,
    #     flights.dest_id,
    #     flights.dep_time_blk,
    #     flights.arr_del15
    # FROM flights
    # JOIN airlines ON airlines.id = flights.airline_id
    # WHERE arr_del15 IS NOT NULL
    #     AND cancelled = 0
    # """

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
        AND cancelled = 0
    """

    df = pd.read_sql(query, engine)

    if df.empty:
        logger.warning("No training data found.")
        return df

    df = df.dropna()
    logger.success(f"{len(df)} total rows loaded before sampling.")

    label_counts = Counter(df["arr_del15"])
    min_class_ratio = min(count / len(df) for count in label_counts.values())

    # Stratified sampling if possible and keep only 10% of data
    if min_class_ratio < 0.05:
        logger.warning("Minority class is under 5%. Disabling stratified sampling.")
        _, df_sampled = train_test_split(df, test_size=0.1, random_state=42)
    else:
        _, df_sampled = train_test_split(
            df, test_size=0.1, stratify=df["arr_del15"], random_state=42
        )

    logger.success(f"{len(df_sampled)} rows returned after 10% stratified sampling.")
    return df_sampled.reset_index(drop=True)
