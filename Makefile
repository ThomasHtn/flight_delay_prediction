# Makefile

# =====================================================================================
# Database
# =====================================================================================

DB_PATH=./dump/flights.db
CSV_PATH=./data/processed/cleaned_data.csv

.PHONY: migrate upgrade seed reset

clear-and-populate-db:
	python scripts/clear_dataset.py

populate-db:
	python scripts/populate_db.py $(CSV_PATH)

# =====================================================================================
# Tests
# =====================================================================================

test:
	pytest -s tests/