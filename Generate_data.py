import os
import random
from faker import Faker
import pandas as pd
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)

# Output directory
OUT = "data"
os.makedirs(OUT, exist_ok=True)

NUM_CUSTOMERS = 200
NUM_PRODUCTS = 50
NUM_ORDERS = 400
MAX_ITEMS_PER_ORDER = 5

# ------------------------
# Generate Customers
# ------------------------
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    customers.append({
        "customer_id": i,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.unique.email(),
        "created_at": fake.date_between(start_date="-3y", end_date="today").isoformat(),
        "country": fake.country()
    })

pd.DataFrame(customers).to_csv(os.path.join(OUT, "customers.csv"), index=False)

# ------------------------
# Generate Products
# ------------------------
products = []
categories = ["Electronics", "Apparel", "Home", "Beauty", "Outdoors"]

for i in range(1, NUM_PRODUCTS + 1):
    products.append({
        "product_id": i,
        "sku": f"SKU-{1000 + i}",
        "name": fake.word().title() + " " + fake.word().title(),
        "category": random.choice(categories),
        "price": round(random.uniform(5.0, 500.0), 2),
        "in_stock": random.randint(0, 200)
    })

pd.DataFrame(products).to_csv(os.path.join(OUT, "products.csv"), index=False)

# ------------------------
# Generate Orders + Order Items
# ------------------------
orders = []
order_items = []
order_id_seq = 1

for i in range(NUM_ORDERS):
    order_id = order_id_seq
    order_id_seq += 1

    cust = random.choice(customers)
    created = fake.date_between(start_date="-365d", end_date="today")
    num_items = random.randint(1, MAX_ITEMS_PER_ORDER)
    total = 0.0

    for j in range(num_items):
        prod = random.choice(products)
        qty = random.randint(1, 4)
        unit_price = prod["price"]
        subtotal = round(unit_price * qty, 2)
        total += subtotal

        order_items.append({
            "order_item_id": len(order_items) + 1,
            "order_id": order_id,
            "product_id": prod["product_id"],
            "quantity": qty,
            "unit_price": unit_price,
            "line_total": subtotal
        })

    orders.append({
        "order_id": order_id,
        "customer_id": cust["customer_id"],
        "order_date": created.isoformat(),
        "order_total": round(total, 2),
        "status": random.choice(["processing", "shipped", "delivered", "cancelled"])
    })

pd.DataFrame(orders).to_csv(os.path.join(OUT, "orders.csv"), index=False)
pd.DataFrame(order_items).to_csv(os.path.join(OUT, "order_items.csv"), index=False)

# ------------------------
# Generate Shipments
# ------------------------
shipments = []

for o in orders:
    shipped_at = None
    if o["status"] in ("shipped", "delivered"):
        shipped_at = (
            datetime.fromisoformat(o["order_date"])
            + timedelta(days=random.randint(1, 7))
        ).isoformat()

    shipments.append({
        "shipment_id": o["order_id"],
        "order_id": o["order_id"],
        "shipped_at": shipped_at,
        "carrier": random.choice(["DHL", "FedEx", "UPS", "BlueDart"]),
        "tracking_number": fake.bothify(text="??######")
    })

pd.DataFrame(shipments).to_csv(os.path.join(OUT, "shipments.csv"), index=False)

print("Synthetic e-commerce data generated in /data/")
