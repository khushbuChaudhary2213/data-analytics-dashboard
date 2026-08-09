import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE = os.path.join(DATA_DIR, "analytics.db")


def get_db_connection():
    return sqlite3.connect(DATABASE)


def init_db():
    try:
        conn = get_db_connection()
        conn.execute("""
                        CREATE TABLE IF NOT EXISTS analytics_data (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            order_id TEXT,
                            customer_id TEXT,
                            customer_name TEXT,
                            product_id TEXT,
                            product_name TEXT,
                            category TEXT,
                            quantity INTEGER,
                            price REAL,
                            revenue REAL,
                            order_date TEXT,
                            shipment_id TEXT,
                            delivery_days INTEGER,
                            status TEXT
                        )
                    """)

        conn.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id TEXT,
                    customer_id TEXT,
                    customer_name TEXT,
                    product_id TEXT,
                    quantity INTEGER,
                    price REAL,
                    order_date TEXT
                )
            """)

        conn.execute("""
                    CREATE TABLE IF NOT EXISTS products (
                        product_id TEXT,
                        product_name TEXT,
                        category TEXT
                    )
                """)

        conn.execute("""
                    CREATE TABLE IF NOT EXISTS shipments (
                        shipment_id TEXT,
                        order_id TEXT,
                        delivery_days INTEGER,
                        status TEXT
                    )
                """)
        conn.commit()
    except Exception as e:
        print("DATABASE ERROR: ", e)
    finally:
        conn.close()
