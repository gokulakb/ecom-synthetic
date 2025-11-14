# Ecom Synthetic Demo

1. Install deps:
   pip install -r requirements.txt

2. Generate csv files:
   python generate_data.py
   -> CSVs are in data/

3. Ingest into sqlite:
   python ingest_to_sqlite.py
   -> ecom.db created

4. Run queries:
   sqlite3 ecom.db < queries.sql
   or use any sqlite client (or Python / pandas) to run queries.

Git: add/commit/push (see below).
