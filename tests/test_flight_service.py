import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from database.services.flight_service import get_all_flights


def test_get_all_flights_returns_data():
    # Call the service function to retrieve flights
    flights = get_all_flights(limit=5)

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
