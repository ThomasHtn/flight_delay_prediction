import os
import sys

import pandas as pd

# Add project root to sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.services.flight_service import (
    get_all_airlines,
    get_all_airports,
    get_all_flights,
    load_training_data,
)

# ───────────────────────────────────────────────────────────────
# Test: Flight Data
# ───────────────────────────────────────────────────────────────


def test_get_all_flights_returns_data():
    """
    Ensure get_all_flights() returns a non-empty list of valid flight objects.
    """
    flights = get_all_flights(limit=5)

    for f in flights:
        print({k: v for k, v in vars(f).items() if not k.startswith("_")})

    assert isinstance(flights, list), "Expected a list of flights"
    assert len(flights) > 0, "No flights found in database"

    for flight in flights:
        assert hasattr(flight, "origin_id")
        assert hasattr(flight, "dest_id")
        assert hasattr(flight, "year")


# ───────────────────────────────────────────────────────────────
# Test: Airport Data
# ───────────────────────────────────────────────────────────────


def test_get_all_airports_returns_data():
    """
    Ensure get_all_airports() returns valid airport objects with expected attributes.
    """
    airports = get_all_airports(limit=1)

    for a in airports:
        print({k: v for k, v in vars(a).items() if not k.startswith("_")})

    assert isinstance(airports, list), "Expected a list of airports"
    assert len(airports) > 0, "No airports found in database"

    for airport in airports:
        assert hasattr(airport, "code")
        assert hasattr(airport, "city_name")
        assert hasattr(airport, "state_abbr")


# ───────────────────────────────────────────────────────────────
# Test: Airline Data
# ───────────────────────────────────────────────────────────────


def test_get_all_airlines_returns_data():
    """
    Ensure get_all_airlines() returns valid airline records.
    """
    airlines = get_all_airlines(limit=1)

    for a in airlines:
        print({k: v for k, v in vars(a).items() if not k.startswith("_")})

    assert isinstance(airlines, list), "Expected a list of airlines"
    assert len(airlines) > 0, "No airlines found in database"

    for airline in airlines:
        assert hasattr(airline, "unique_carrier")
        assert hasattr(airline, "airline_id")
        assert hasattr(airline, "carrier")


# ───────────────────────────────────────────────────────────────
# Test: Training Data Loader
# ───────────────────────────────────────────────────────────────


def test_load_training_data_returns_valid_dataframe():
    """
    Ensure load_training_data() returns a well-formed DataFrame with expected columns and labels.
    """
    df = load_training_data()

    assert isinstance(df, pd.DataFrame), "Expected a pandas DataFrame"
    assert not df.empty, "Returned DataFrame is empty"

    # Validate presence of all required columns
    expected_columns = {
        "month",
        "day_of_week",
        "crs_dep_time",
        "crs_arr_time",
        "crs_elapsed_time",
        "distance",
        "unique_carrier",
        "origin",
        "dest",
        "dep_time_blk",
        "arr_del15",
    }
    actual_columns = set(df.columns)
    missing_columns = expected_columns - actual_columns
    assert not missing_columns, f"Missing columns: {missing_columns}"

    # Check binary nature of the target column
    assert set(df["arr_del15"].unique()).issubset({0, 1}), (
        "arr_del15 must be binary (0 or 1)"
    )

    print(df.head())
