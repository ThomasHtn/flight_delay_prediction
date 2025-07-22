import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

from database.base import SessionLocal, engine
from database.models.flight import Flight


def populate_from_csv(csv_path: str):
    """Populate the database with flights from a cleaned CSV file."""
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.lower()  # Normalize column names

    session: Session = SessionLocal()
    try:
        for _, row in df.iterrows():
            flight = Flight(**row.to_dict())
            session.add(flight)

        session.commit()
        print("✅ Data inserted successfully.")

        # 🔍 Show first 5 rows directly from the DB (real state after commit)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM flights LIMIT 5"))
            rows = result.mappings().all()
            print("\n📊 First 5 rows in the 'flights' table:")
            for row in rows:
                print(dict(row))

    except Exception as e:
        session.rollback()
        print("❌ Error during insert:", e)
    finally:
        session.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide the CSV path as an argument.")
        sys.exit(1)

    csv_path = sys.argv[1]
    populate_from_csv(csv_path)
