import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


# -----------------------------------------
# BASIC SETTINGS
# -----------------------------------------

random.seed(42)

DATA_FOLDER = Path(__file__).parent

NUM_SUPPLIERS = 20
NUM_PRODUCTS = 60
NUM_ORDERS = 600


# -----------------------------------------
# 1. SUPPLIERS
# -----------------------------------------

supplier_names = [
    "Alpha Electronics",
    "Vertex Components",
    "Nova Industrial",
    "Prime Logistics",
    "Global Tech Supplies",
    "Apex Manufacturing",
    "Bright Source",
    "United Components",
    "Reliable Goods",
    "Metro Supply Co",
    "Eastern Traders",
    "Smart Parts India",
    "BlueLine Supplies",
    "Rapid Components",
    "FutureTech Industries",
    "Evergreen Supplies",
    "Dynamic Distribution",
    "Precision Parts",
    "Summit Suppliers",
    "Core Industrial"
]

locations = [
    "Hyderabad",
    "Bengaluru",
    "Chennai",
    "Mumbai",
    "Pune",
    "Delhi",
    "Ahmedabad",
    "Kolkata"
]

supplier_categories = [
    "Electronics",
    "Industrial",
    "Packaging",
    "Components",
    "Technology"
]


suppliers = []

for i in range(NUM_SUPPLIERS):

    supplier_id = f"SUP{i + 1:03d}"

    # Create different supplier performance levels
    if i < 4:
        performance_profile = "High Risk"
    elif i < 9:
        performance_profile = "Medium Risk"
    else:
        performance_profile = "Low Risk"

    suppliers.append({
        "supplier_id": supplier_id,
        "supplier_name": supplier_names[i],
        "location": random.choice(locations),
        "supplier_category": random.choice(supplier_categories),
        "performance_profile": performance_profile
    })


suppliers_df = pd.DataFrame(suppliers)


# -----------------------------------------
# 2. PRODUCTS
# -----------------------------------------

product_names = [
    "Wireless Keyboard",
    "Wireless Mouse",
    "USB-C Hub",
    "Bluetooth Speaker",
    "Power Adapter",
    "Laptop Stand",
    "Web Camera",
    "Mechanical Keyboard",
    "Monitor Stand",
    "HDMI Cable",
    "Ethernet Cable",
    "SSD Drive",
    "RAM Module",
    "Power Bank",
    "Smart Sensor",
    "LED Panel",
    "Network Switch",
    "Router",
    "Barcode Scanner",
    "Thermal Printer"
]

categories = [
    "Electronics",
    "Computer Accessories",
    "Networking",
    "Storage",
    "Office Equipment"
]

products = []

for i in range(NUM_PRODUCTS):

    product_id = f"PRD{i + 1:03d}"

    product_name = random.choice(product_names)

    category = random.choice(categories)

    supplier = random.choice(suppliers)

    unit_cost = round(random.uniform(200, 15000), 2)

    selling_price = round(
        unit_cost * random.uniform(1.15, 1.60),
        2
    )

    products.append({
        "product_id": product_id,
        "product_name": product_name,
        "category": category,
        "supplier_id": supplier["supplier_id"],
        "unit_cost": unit_cost,
        "selling_price": selling_price
    })


products_df = pd.DataFrame(products)


# -----------------------------------------
# 3. INVENTORY
# -----------------------------------------

inventory = []

for _, product in products_df.iterrows():

    average_daily_demand = random.randint(5, 100)

    lead_time_days = random.randint(2, 20)

    reorder_level = (
        average_daily_demand
        * lead_time_days
        * random.uniform(1.0, 1.5)
    )

    stock_condition = random.choice([
        "Healthy",
        "Healthy",
        "Healthy",
        "Low",
        "Overstock"
    ])

    if stock_condition == "Healthy":

        current_stock = int(
            reorder_level * random.uniform(1.2, 3.0)
        )

    elif stock_condition == "Low":

        current_stock = int(
            reorder_level * random.uniform(0.2, 0.8)
        )

    else:

        current_stock = int(
            reorder_level * random.uniform(3.0, 6.0)
        )

    inventory.append({
        "product_id": product["product_id"],
        "current_stock": current_stock,
        "reorder_level": round(reorder_level, 0),
        "average_daily_demand": average_daily_demand,
        "lead_time_days": lead_time_days
    })


inventory_df = pd.DataFrame(inventory)


# -----------------------------------------
# 4. ORDERS
# -----------------------------------------

orders = []

start_date = datetime(2025, 10, 1)
end_date = datetime(2026, 9, 30)

date_range_days = (end_date - start_date).days


for i in range(NUM_ORDERS):

    product = products_df.sample(1).iloc[0]

    supplier_id = product["supplier_id"]

    order_date = start_date + timedelta(
        days=random.randint(0, date_range_days)
    )

    quantity = random.randint(1, 100)

    unit_cost = product["unit_cost"]

    supplier_profile = suppliers_df[
        suppliers_df["supplier_id"] == supplier_id
    ]["performance_profile"].iloc[0]

    # High-risk suppliers have a higher defect probability
    if supplier_profile == "High Risk":
        defect_probability = 0.12
    elif supplier_profile == "Medium Risk":
        defect_probability = 0.06
    else:
        defect_probability = 0.02

    defect_flag = (
        1 if random.random() < defect_probability else 0
    )

    orders.append({
        "order_id": f"ORD{i + 1:05d}",
        "supplier_id": supplier_id,
        "product_id": product["product_id"],
        "order_date": order_date.strftime("%Y-%m-%d"),
        "quantity": quantity,
        "unit_cost": unit_cost,
        "defect_flag": defect_flag
    })


orders_df = pd.DataFrame(orders)


# -----------------------------------------
# 5. SHIPMENTS
# -----------------------------------------

shipments = []

destinations = [
    "Hyderabad",
    "Bengaluru",
    "Chennai",
    "Mumbai",
    "Pune",
    "Delhi"
]


for i, order in orders_df.iterrows():

    supplier_id = order["supplier_id"]

    supplier_profile = suppliers_df[
        suppliers_df["supplier_id"] == supplier_id
    ]["performance_profile"].iloc[0]

    order_date = datetime.strptime(
        order["order_date"],
        "%Y-%m-%d"
    )

    expected_days = random.randint(3, 10)

    expected_delivery_date = (
        order_date + timedelta(days=expected_days)
    )

    # Higher-risk suppliers have more delivery delays
    if supplier_profile == "High Risk":

        delay = random.choices(
            [0, 1, 2, 3, 5, 7, 10],
            weights=[10, 8, 10, 10, 8, 5, 3]
        )[0]

    elif supplier_profile == "Medium Risk":

        delay = random.choices(
            [0, 1, 2, 3, 5, 7],
            weights=[20, 15, 12, 8, 4, 2]
        )[0]

    else:

        delay = random.choices(
            [0, 1, 2, 3, 5],
            weights=[45, 20, 10, 5, 2]
        )[0]

    actual_delivery_date = (
        expected_delivery_date
        + timedelta(days=delay)
    )

    if delay == 0:
        delivery_status = "On Time"
    else:
        delivery_status = "Delayed"

    supplier = suppliers_df[
        suppliers_df["supplier_id"] == supplier_id
    ].iloc[0]

    shipments.append({
        "shipment_id": f"SHP{i + 1:05d}",
        "order_id": order["order_id"],
        "supplier_id": supplier_id,
        "product_id": order["product_id"],
        "origin": supplier["location"],
        "destination": random.choice(destinations),
        "order_date": order["order_date"],
        "expected_delivery_date": expected_delivery_date.strftime(
            "%Y-%m-%d"
        ),
        "actual_delivery_date": actual_delivery_date.strftime(
            "%Y-%m-%d"
        ),
        "delivery_status": delivery_status,
        "delay_days": delay
    })


shipments_df = pd.DataFrame(shipments)


# -----------------------------------------
# SAVE THE CSV FILES
# -----------------------------------------

suppliers_df.to_csv(
    DATA_FOLDER / "suppliers.csv",
    index=False
)

products_df.to_csv(
    DATA_FOLDER / "products.csv",
    index=False
)

inventory_df.to_csv(
    DATA_FOLDER / "inventory.csv",
    index=False
)

orders_df.to_csv(
    DATA_FOLDER / "orders.csv",
    index=False
)

shipments_df.to_csv(
    DATA_FOLDER / "shipments.csv",
    index=False
)


# -----------------------------------------
# SHOW RESULT
# -----------------------------------------

print()
print("=" * 50)
print("SUPPLYSENSE DATASET GENERATION COMPLETE")
print("=" * 50)

print(f"Suppliers : {len(suppliers_df)}")
print(f"Products  : {len(products_df)}")
print(f"Inventory : {len(inventory_df)}")
print(f"Orders    : {len(orders_df)}")
print(f"Shipments : {len(shipments_df)}")

print()
print("5 CSV files created successfully.")
print("=" * 50)