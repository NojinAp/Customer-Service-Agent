import csv
import random
from datetime import datetime, timedelta

random.seed(42)

PRODUCTS = [
    {"name": "8oz Deli", "sku": "DR-508", "category": "Deli Containers"},
    {"name": "12oz Deli", "sku": "DR-512", "category": "Deli Containers"},
    {"name": "Deli Overcap Lid", "sku": "DR-ORL", "category": "Lids"},
    {"name": "Deli Recessed Lid", "sku": "DR-RL", "category": "Lids"},
    {"name": "12oz Rectangle", "sku": "CR-811", "category": "Rectangle Containers"},
    {"name": "16oz Deli", "sku": "DR-516", "category": "Deli Containers"},
    {"name": "16oz Rectangle", "sku": "CR-815", "category": "Rectangle Containers"},
    {"name": "18oz Round", "sku": "CO-518", "category": "Round Containers"},
    {"name": "24oz Round", "sku": "CO-624", "category": "Round Containers"},
    {"name": "24oz Round Baseball", "sku": "CO-624-BAS", "category": "Specialty Containers"},
    {"name": "24oz Round Basketball", "sku": "CO-624-BKT", "category": "Specialty Containers"},
    {"name": "24oz Round Soccer", "sku": "CO-624-SOC", "category": "Specialty Containers"},
    {"name": "28oz Rectangle", "sku": "CR-927", "category": "Rectangle Containers"},
    {"name": "28oz Rectangle", "sku": "CR-928", "category": "Rectangle Containers"},
    {"name": "28oz Rectangle 2-Compartment", "sku": "CR-M-2932", "category": "Rectangle Containers"},
]

CUSTOMERS = [
    ("C001", "Fresh Farms Deli"),
    ("C002", "Metro Grocery Co."),
    ("C003", "Sunrise Catering"),
    ("C004", "GreenLeaf Foods"),
    ("C005", "Urban Meal Prep"),
    ("C006", "Harvest Table"),
    ("C007", "QuickBite Kitchens"),
    ("C008", "Northside Deli"),
    ("C009", "Pacific Foods Ltd."),
    ("C010", "Central Market Group"),
]

STATUSES = ["Processing", "Confirmed", "Shipped", "Delivered", "Cancelled"]
CARRIERS = ["FedEx", "UPS", "DHL"]

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

start = datetime(2025, 1, 1)
end = datetime(2026, 7, 1)

# Generate orders
orders = []
for i in range(1, 101):
    customer = random.choice(CUSTOMERS)
    product = random.choice(PRODUCTS)
    order_date = random_date(start, end)
    status = random.choice(STATUSES)
    quantity = random.randint(100, 5000)  # Bulk packaging orders
    unit_price = round(random.uniform(0.05, 0.50), 3)  # Per unit price
    orders.append({
        "order_id": f"ORD-{i:04d}",
        "customer_id": customer[0],
        "customer_name": customer[1],
        "product_name": product["name"],
        "sku": product["sku"],
        "category": product["category"],
        "quantity": quantity,
        "unit_price": unit_price,
        "total_price": round(quantity * unit_price, 2),
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