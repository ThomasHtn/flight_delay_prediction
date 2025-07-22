import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

bdd_file_path = os.path.join(BASE_DIR, "dump", "flights.db")
engine = create_engine("sqlite:///" + bdd_file_path)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
