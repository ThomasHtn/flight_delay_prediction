import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from database.services.flight_service import (
    get_all_airlines,
    get_all_airports,
    get_all_flights,
)


def test_get_all_flights_returns_data():
    # Call the service function to retrieve flights
    flights = get_all_flights(limit=1)

    # Display the first retrieved records as clean dictionaries
    for f in flights:
        print({k: v for k, v in vars(f).items() if not k.startswith("_")})

    # Check that the result is a list
    assert isinstance(flights, list), "Expected a list of flights"

    # Check that the list is not empty
    assert len(flights) > 0, "No flights found in database"

    # Check that each flight has the expected attributes
    for flight in flights:
        assert hasattr(flight, "origin")
        assert hasattr(flight, "dest")
        assert hasattr(flight, "year")


def test_get_all_airports_returns_data():
    # Call the service function to retrieve airports
    airports = get_all_airports(limit=1)

    # Display the first retrieved records as clean dictionaries
    for a in airports:
        print({k: v for k, v in vars(a).items() if not k.startswith("_")})

    # Check that the result is a list
    assert isinstance(airports, list), "Expected a list of airports"

    # Check that the list is not empty
    assert len(airports) > 0, "No airports found in database"

    # Check that each airport has the expected attributes
    for airport in airports:
        assert hasattr(airport, "code")
        assert hasattr(airport, "city_name")
        assert hasattr(airport, "state_abbr")


def test_get_all_airlines_returns_data():
    # Call the service function to retrieve airlines
    airlines = get_all_airlines(limit=1)

    # Display the first retrieved records as clean dictionaries
    for a in airlines:
        print({k: v for k, v in vars(a).items() if not k.startswith("_")})

    # Check that the result is a list
    assert isinstance(airlines, list), "Expected a list of airlines"

    # Check that the list is not empty
    assert len(airlines) > 0, "No airlines found in database"

    # Check that each airline has the expected attributes
    for airline in airlines:
        assert hasattr(airline, "unique_carrier")
        assert hasattr(airline, "airline_id")
        assert hasattr(airline, "carrier")
