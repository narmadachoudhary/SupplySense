import sqlite3
from pathlib import Path

import pandas as pd


# -----------------------------------------
# PATH SETTINGS
# -----------------------------------------

PROJECT_FOLDER = Path(__file__).resolve().parent.parent

DATA_FOLDER = PROJECT_FOLDER / "data"
DATABASE_FOLDER = PROJECT_FOLDER / "database"

DATABASE_FILE = DATABASE_FOLDER / "supplysense.db"


# -----------------------------------------
# CREATE DATABASE FOLDER
# -----------------------------------------

DATABASE_FOLDER.mkdir(exist_ok=True)


# -----------------------------------------
# CONNECT TO SQLITE DATABASE
# -----------------------------------------

connection = sqlite3.connect(DATABASE_FILE)


# -----------------------------------------
# CSV FILE PATHS
# -----------------------------------------

suppliers_file = DATA_FOLDER / "suppliers.csv"
products_file = DATA_FOLDER / "products.csv"
inventory_file = DATA_FOLDER / "inventory.csv"
orders_file = DATA_FOLDER / "orders.csv"
shipments_file = DATA_FOLDER / "shipments.csv"


# -----------------------------------------
# READ CSV FILES
# -----------------------------------------

suppliers_df = pd.read_csv(suppliers_file)
products_df = pd.read_csv(products_file)
inventory_df = pd.read_csv(inventory_file)
orders_df = pd.read_csv(orders_file)
shipments_df = pd.read_csv(shipments_file)


# -----------------------------------------
# INSERT DATA INTO SQLITE TABLES
# -----------------------------------------

suppliers_df.to_sql(
    "suppliers",
    connection,
    if_exists="replace",
    index=False
)

products_df.to_sql(
    "products",
    connection,
    if_exists="replace",
    index=False
)

inventory_df.to_sql(
    "inventory",
    connection,
    if_exists="replace",
    index=False
)

orders_df.to_sql(
    "orders",
    connection,
    if_exists="replace",
    index=False
)

shipments_df.to_sql(
    "shipments",
    connection,
    if_exists="replace",
    index=False
)


# -----------------------------------------
# CLOSE DATABASE CONNECTION
# -----------------------------------------

connection.close()


# -----------------------------------------
# SUCCESS MESSAGE
# -----------------------------------------

print()
print("=" * 55)
print("SUPPLYSENSE SQLITE DATABASE CREATED SUCCESSFULLY")
print("=" * 55)

print(f"Database location: {DATABASE_FILE}")

print()
print("Tables created:")
print("1. suppliers")
print("2. products")
print("3. inventory")
print("4. orders")
print("5. shipments")

print()
print("Records inserted:")
print(f"Suppliers : {len(suppliers_df)}")
print(f"Products  : {len(products_df)}")
print(f"Inventory : {len(inventory_df)}")
print(f"Orders    : {len(orders_df)}")
print(f"Shipments : {len(shipments_df)}")

print("=" * 55)