import csv
import random
from datetime import datetime, timedelta

random.seed(42)

PRODUCTS = [
    "Expedition Parka", "Langford Parka", "Chilliwack Bomber",
    "Hybridge Lite Jacket", "Snow Mantra Parka", "Freestyle Vest",
    "Lodge Hoody", "Timber Shell Jacket"
]

CUSTOMERS = [
    ("C001", "Alice Martin"), ("C002", "James Lee"), ("C003", "Priya Sharma"),
    ("C004", "Noah Brown"), ("C005", "Emma Wilson"), ("C006", "Liam Chen"),
    ("C007", "Olivia Davis"), ("C008", "Ethan Moore"), ("C009", "Sophia Taylor"),
    ("C010", "Lucas Anderson")
]

STATUSES = ["Processing", "Confirmed", "Shipped", "Delivered", "Cancelled"]
CARRIERS = ["FedEx", "UPS", "DHL"]
SHIP_STATUSES = ["In Transit", "Out for Delivery", "Delivered", "Delayed", "Pending"]

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

start = datetime(2025, 1, 1)
end = datetime(2026, 7, 1)

# Generate orders
orders = []
for i in range(1, 101):
    customer = random.choice(CUSTOMERS)
    order_date = random_date(start, end)
    status = random.choice(STATUSES)
    orders.append({
        "order_id": f"ORD-{i:04d}",
        "customer_id": customer[0],
        "customer_name": customer[1],
        "product": random.choice(PRODUCTS),
        "quantity": random.randint(1, 3),
        "price": round(random.uniform(500, 1800), 2),
        "order_date": order_date.strftime("%Y-%m-%d"),
        "status": status
    })

# Generate shipments
shipments = []
for order in orders:
    if order["status"] in ["Shipped", "Delivered"]:
        ship_date = datetime.strptime(order["order_date"], "%Y-%m-%d") + timedelta(days=random.randint(1, 5))
        est_delivery = ship_date + timedelta(days=random.randint(2, 7))
        shipments.append({
            "shipment_id": f"SHP-{order['order_id'][4:]}",
            "order_id": order["order_id"],
            "carrier": random.choice(CARRIERS),
            "tracking_number": f"TRK{random.randint(100000000, 999999999)}",
            "ship_date": ship_date.strftime("%Y-%m-%d"),
            "estimated_delivery": est_delivery.strftime("%Y-%m-%d"),
            "status": "Delivered" if order["status"] == "Delivered" else random.choice(["In Transit", "Out for Delivery", "Delayed"])
        })

# Write CSVs
with open("orders.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=orders[0].keys())
    writer.writeheader()
    writer.writerows(orders)

with open("shipments.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=shipments[0].keys())
    writer.writeheader()
    writer.writerows(shipments)

print(f"Generated {len(orders)} orders and {len(shipments)} shipments")