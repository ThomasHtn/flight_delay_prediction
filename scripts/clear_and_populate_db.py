import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import date

import pandas as pd
from sklearn.model_selection import train_test_split
from sqlalchemy.orm import Session

from database.base import SessionLocal
from database.models.airline import Airline
from database.models.airports import Airport
from database.models.flight import Flight


def agregate_and_clear_dataset():
    """Load and clean raw CSV files for the year 2016, return a clean sampled DataFrame."""
    dfs = []

    # Load monthly CSV files
    for month in range(1, 13):
        file = f"data/raw/2016_{month:02}.csv"
        if not os.path.exists(file):
            print(f"File not found: {file}")
            continue
        try:
            tmp = pd.read_csv(file, on_bad_lines="warn", low_memory=False)
            dfs.append(tmp)
            print(f"Loaded {file} ✅")
        except pd.errors.ParserError as e:
            print(f"ParserError for {file}: {e}")
        print("-" * 50)

    if not dfs:
        raise ValueError("No files were loaded, stopping execution.")

    # Combine all monthly data into one DataFrame
    full_df = pd.concat(dfs, ignore_index=True)

    # Standardize column names
    full_df.columns = [col.strip().upper() for col in full_df.columns]

    # Remove invalid rows (e.g. corrupted line with MONTH = 20366)
    full_df = full_df[full_df["MONTH"].between(1, 12)]

    # Replace NaN with None (for SQL compatibility)
    full_df = full_df.where(pd.notnull(full_df), None)

    # Convert date-related columns to integers
    columns_to_convert = ["YEAR", "QUARTER", "MONTH", "DAY_OF_MONTH", "DAY_OF_WEEK"]
    for col in columns_to_convert:
        if col in full_df.columns:
            full_df[col] = full_df[col].astype(str).str.strip()
            full_df[col] = pd.to_numeric(full_df[col], errors="coerce")
            full_df[col] = full_df[col].astype("Int64")

    # Convert all non-numeric columns to strings
    for col in full_df.columns:
        if not (
            pd.api.types.is_float_dtype(full_df[col])
            or pd.api.types.is_integer_dtype(full_df[col])
        ):
            full_df[col] = full_df[col].astype(str).str.strip()

    # Ensure the target column is present
    if "ARR_DEL15" not in full_df.columns:
        raise ValueError("ARR_DEL15 column is missing from the dataset.")

    # Drop rows without a valid target value
    full_df = full_df.dropna(subset=["ARR_DEL15"])

    # Stratified sampling (preserve class distribution for ARR_DEL15)
    data = train_test_split(
        full_df, test_size=0.2, stratify=full_df["ARR_DEL15"], random_state=42
    )[1].reset_index(drop=True)

    print(f"Final dataset: {data.shape[0]} rows, {data.shape[1]} columns")
    return data


def insert_airlines(df, session):
    """Insert unique airlines into the database."""
    airline_cols = ["UNIQUE_CARRIER", "AIRLINE_ID", "CARRIER"]
    airlines = df[airline_cols].drop_duplicates()

    for _, row in airlines.iterrows():
        airline = Airline(
            unique_carrier=row["UNIQUE_CARRIER"],
            airline_id=row["AIRLINE_ID"],
            carrier=row["CARRIER"],
        )
        session.merge(airline)  # Upsert logic


def insert_airports(df, session):
    """Insert unique airports (origin and destination) into the database."""
    # Extract and rename origin airport data
    origin_df = df[
        [
            "ORIGIN",
            "ORIGIN_CITY_NAME",
            "ORIGIN_STATE_ABR",
            "ORIGIN_STATE_FIPS",
            "ORIGIN_STATE_NM",
            "ORIGIN_WAC",
        ]
    ].rename(
        columns={
            "ORIGIN": "CODE",
            "ORIGIN_CITY_NAME": "CITY_NAME",
            "ORIGIN_STATE_ABR": "STATE_ABBR",
            "ORIGIN_STATE_FIPS": "STATE_FIPS",
            "ORIGIN_STATE_NM": "STATE_NM",
            "ORIGIN_WAC": "WAC",
        }
    )

    # Extract and rename destination airport data
    dest_df = df[
        [
            "DEST",
            "DEST_CITY_NAME",
            "DEST_STATE_ABR",
            "DEST_STATE_FIPS",
            "DEST_STATE_NM",
            "DEST_WAC",
        ]
    ].rename(
        columns={
            "DEST": "CODE",
            "DEST_CITY_NAME": "CITY_NAME",
            "DEST_STATE_ABBR": "STATE_ABBR",
            "DEST_STATE_FIPS": "STATE_FIPS",
            "DEST_STATE_NM": "STATE_NM",
            "DEST_WAC": "WAC",
        }
    )

    # Combine origin and destination data, and deduplicate
    airports_df = pd.concat([origin_df, dest_df]).drop_duplicates(subset=["CODE"])

    for _, row in airports_df.iterrows():
        airport = Airport(
            code=row["CODE"],
            city_name=row["CITY_NAME"],
            state_abbr=row["STATE_ABBR"],
            state_fips=row["STATE_FIPS"],
            state_name=row["STATE_NM"],
            wac=row["WAC"],
        )
        session.merge(airport)


def insert_flights(df, session):
    """Insert flights linked with valid airline_id and airport_ids"""
    # Normalize keys for matching
    airline_map = {
        a.unique_carrier.strip().upper(): a.id for a in session.query(Airline).all()
    }
    airport_map = {a.code.strip().upper(): a.id for a in session.query(Airport).all()}

    skipped = 0
    inserted = 0

    for _, row in df.iterrows():
        try:
            flight_date = date(
                int(row["YEAR"]), int(row["MONTH"]), int(row["DAY_OF_MONTH"])
            )
        except:
            skipped += 1
            continue

        airline_id = airline_map.get(row["UNIQUE_CARRIER"].strip().upper())
        origin_id = airport_map.get(row["ORIGIN"].strip().upper())
        dest_id = airport_map.get(row["DEST"].strip().upper())

        if not all([airline_id, origin_id, dest_id]):
            skipped += 1
            continue

        flight = Flight(
            year=row["YEAR"],
            quarter=row["QUARTER"],
            month=row["MONTH"],
            day_of_month=row["DAY_OF_MONTH"],
            day_of_week=row["DAY_OF_WEEK"],
            fl_date=flight_date,
            airline_id=airline_id,
            flight_num=row.get("FL_NUM"),
            tail_num=row.get("TAIL_NUM"),
            origin_id=origin_id,
            dest_id=dest_id,
            crs_dep_time=row.get("CRS_DEP_TIME"),
            dep_time_blk=row.get("DEP_TIME_BLK"),
            taxi_out=row.get("TAXI_OUT"),
            taxi_in=row.get("TAXI_IN"),
            crs_arr_time=row.get("CRS_ARR_TIME"),
            arr_del15=row.get("ARR_DEL15"),
            crs_elapsed_time=row.get("CRS_ELAPSED_TIME"),
            distance=row.get("DISTANCE"),
            distance_group=row.get("DISTANCE_GROUP"),
            carrier_delay=row.get("CARRIER_DELAY"),
            weather_delay=row.get("WEATHER_DELAY"),
            nas_delay=row.get("NAS_DELAY"),
            security_delay=row.get("SECURITY_DELAY"),
            late_aircraft_delay=row.get("LATE_AIRCRAFT_DELAY"),
            first_dep_time=row.get("FIRST_DEP_TIME"),
            total_add_gtime=row.get("TOTAL_ADD_GTIME"),
            longest_add_gtime=row.get("LONGEST_ADD_GTIME"),
            cancelled=bool(row.get("CANCELLED"))
            if row.get("CANCELLED") is not None
            else None,
            cancellation_code=row.get("CANCELLATION_CODE"),
            diverted=bool(row.get("DIVERTED"))
            if row.get("DIVERTED") is not None
            else None,
        )
        session.add(flight)
        inserted += 1

    print(f"Inserted flights: {inserted} | Skipped flights: {skipped}")


if __name__ == "__main__":
    # Load and prepare dataset
    df = agregate_and_clear_dataset()

    # Initialize DB session
    session: Session = SessionLocal()

    try:
        # Insert all data in the right order
        insert_airlines(df, session)
        session.flush()

        insert_airports(df, session)
        session.flush()

        insert_flights(df, session)

        session.commit()
        print("✅ All data successfully inserted into the database.")
    except Exception as e:
        session.rollback()
        print("❌ Error during insertion:", e)
    finally:
        session.close()
