import sqlite3
from pathlib import Path

import pandas as pd


# -----------------------------------------
# DATABASE PATH
# -----------------------------------------

PROJECT_FOLDER = Path(__file__).resolve().parent.parent

DATABASE_FILE = PROJECT_FOLDER / "database" / "supplysense.db"


# -----------------------------------------
# DATABASE CONNECTION
# -----------------------------------------

def get_connection():
    """
    Create and return a connection to the
    SupplySense SQLite database.
    """
    return sqlite3.connect(DATABASE_FILE)


# -----------------------------------------
# LOAD SUPPLIERS
# -----------------------------------------

def load_suppliers():
    connection = get_connection()

    query = "SELECT * FROM suppliers"

    data = pd.read_sql_query(query, connection)

    connection.close()

    return data


# -----------------------------------------
# LOAD PRODUCTS
# -----------------------------------------

def load_products():
    connection = get_connection()

    query = "SELECT * FROM products"

    data = pd.read_sql_query(query, connection)

    connection.close()

    return data


# -----------------------------------------
# LOAD INVENTORY
# -----------------------------------------

def load_inventory():
    connection = get_connection()

    query = "SELECT * FROM inventory"

    data = pd.read_sql_query(query, connection)

    connection.close()

    return data


# -----------------------------------------
# LOAD ORDERS
# -----------------------------------------

def load_orders():
    connection = get_connection()

    query = "SELECT * FROM orders"

    data = pd.read_sql_query(query, connection)

    connection.close()

    return data


# -----------------------------------------
# LOAD SHIPMENTS
# -----------------------------------------

def load_shipments():
    connection = get_connection()

    query = "SELECT * FROM shipments"

    data = pd.read_sql_query(query, connection)

    connection.close()

    return data