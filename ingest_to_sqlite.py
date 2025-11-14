# ingest_to_sqlite.py
import sqlite3
import pandas as pd
import os

DB = "ecom.db"
DATA_DIR = "data"

conn = sqlite3.connect(DB)
cur = conn.cursor()

# Create tables
cur.executescript("""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT UNIQUE,
    created_at TEXT,
    country TEXT
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    sku TEXT,
    name TEXT,
    category TEXT,
    price REAL,
    in_stock INTEGER
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    order_total REAL,
    status TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL,
    line_total REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS shipments (
    shipment_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    shipped_at TEXT,
    carrier TEXT,
    tracking_number TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
""")
conn.commit()

# Helper to load a CSV to a table using pandas
def load_csv_to_table(csv_path, table_name):
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists='append', index=False)

# Load files (ensure files exist)
files = {
    "customers.csv": "customers",
    "products.csv": "products",
    "orders.csv": "orders",
    "order_items.csv": "order_items",
    "shipments.csv": "shipments",
}

for fname, table in files.items():
    path = os.path.join(DATA_DIR, fname)
    if os.path.exists(path):
        print(f"Loading {fname} -> {table}")
        load_csv_to_table(path, table)
    else:
        print(f"Missing {path}, skipping.")

conn.commit()
conn.close()
print("Ingestion complete. DB:", DB)
