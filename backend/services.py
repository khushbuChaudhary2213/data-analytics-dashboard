import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()


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
    df["is_delayed"] = df["status"].str.lower() == "delayed"

    return df


rest_countries_api_key = os.getenv("REST_COUNTRIES_API_KEY")


def get_country_currency(country):
    try:
        url = f"https://api.restcountries.com/countries/v5/names.common/{country}"

        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {rest_countries_api_key}"},
            timeout=10,
        )
        if response.status_code != 200:
            raise Exception("Could not find country")

        country_data = response.json()
        objects = country_data["data"]["objects"][0]
        if not objects:
            raise Exception("Country not found")

        currencies = objects["currencies"][0]
        currency_code = currencies["code"]
        currency_name = currencies["name"]
        currency_symbol = currencies["symbol"]
        return {
            "currency_code": currency_code,
            "currency_name": currency_name,
            "currency_symbol": currency_symbol,
        }
    except Exception as e:
        return {"status": False, "message": str(e)}


def get_exchange_rate(from_currency, to_currency):
    try:
        if from_currency == to_currency:
            return 1

        url = "https://api.restcountries.com/currencies/v1/convert"

        response = requests.get(
            url,
            params={
                "from": from_currency,
                "to": to_currency,
                "amount": 1,
            },
            headers={"Authorization": f"Bearer {rest_countries_api_key}"},
            timeout=10,
        )

        if response.status_code != 200:
            raise Exception("Currency conversion failed")

        data = response.json()

        return float(data["data"]["objects"][0]["rate"])

    except Exception as e:
        raise Exception(f"Currency conversion failed: {str(e)}")
