import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


def get_db_connection():
    return engine


def init_db():
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                            CREATE TABLE IF NOT EXISTS analytics_data (
                                id SERIAL PRIMARY KEY,
                                order_id TEXT,
                                customer_id TEXT,
                                customer_name TEXT,
                                product_id TEXT,
                                product_name TEXT,
                                category TEXT,
                                quantity INTEGER,
                                price DOUBLE PRECISION,
                                revenue DOUBLE PRECISION,
                                order_date TEXT,
                                shipment_id TEXT,
                                delivery_days INTEGER,
                                is_delayed BOOLEAN,
                                status TEXT
                            )
                        """))

            conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS orders (
                        order_id TEXT,
                        customer_id TEXT,
                        customer_name TEXT,
                        product_id TEXT,
                        quantity INTEGER,
                        price DOUBLE PRECISION,
                        order_date TEXT
                    )
                """))

            conn.execute(text("""
                        CREATE TABLE IF NOT EXISTS products (
                            product_id TEXT,
                            product_name TEXT,
                            category TEXT
                        )
                    """))

            conn.execute(text("""
                        CREATE TABLE IF NOT EXISTS shipments (
                            shipment_id TEXT,
                            order_id TEXT,
                            delivery_days INTEGER,
                            status TEXT
                        )
                    """))
            print("Database initialized successfully.")

    except Exception as e:
        print("DATABASE ERROR: ", e)
    finally:
        if conn:
            conn.close()
