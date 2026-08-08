import pandas as pd


def flatten_orders(data):
    flattened_data = []

    for order in data["orders"]:
        for item in order["items"]:

            flattened_data.append(
                {
                    "order_id": order["order_id"],
                    "customer_id": order["customer"]["id"],
                    "customer_name": order["customer"]["name"],
                    "product_id": item["product_id"],
                    "quantity": item["qty"],
                    "price": item["price"],
                    "order_date": order["order_date"],
                }
            )

    return flattened_data


def parse_shipments(root):
    shipments = []

    for shipment in root.findall("shipment"):
        shipments.append(
            {
                "shipment_id": shipment.find("shipment_id").text,
                "order_id": shipment.find("order_id").text,
                "delivery_days": int(shipment.find("delivery_days").text),
                "status": shipment.find("status").text,
            }
        )

    return shipments


def merge_data(orders, products, shipments):
    merged = pd.merge(orders, products, on="product_id", how="left")
    merged = pd.merge(merged, shipments, on="order_id", how="left")

    return merged


def clean_data(df):
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["delivery_days"] = pd.to_numeric(df["delivery_days"], errors="coerce")

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    # If Main info is missing simply drop that column
    df = df.dropna(subset=["order_id", "product_id"])

    # Filling NA optional text field
    df["product_name"] = df["product_name"].fillna("Unknown")
    df["category"] = df["category"].fillna("Unknown")
    df["status"] = df["status"].fillna("Unknown")

    # Added new column for aggregation
    df["revenue"] = df["quantity"] * df["price"]

    return df
