from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
import os
from data.store import storedata
from services import merge_data, clean_data, get_exchange_rate
from database import get_db_connection
import pandas as pd

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")

load_dotenv()


@analytics_bp.route("/data", methods=["GET"])
def analytics_data():
    try:
        conn = get_db_connection()
        orders = pd.read_sql("SELECT * FROM orders", conn)
        products = pd.read_sql("SELECT * FROM products", conn)
        shipments = pd.read_sql("SELECT * FROM shipments", conn)

        if orders.empty or products.empty or shipments.empty:
            return (
                jsonify(
                    {"success": False, "message": "Please upload all three files first"}
                ),
                400,
            )

        merged_data = merge_data(orders, products, shipments)
        cleaned_data = clean_data(merged_data)

        conn = get_db_connection()

        cleaned_data.to_sql("analytics_data", conn, if_exists="replace", index=False)

        conn.close()
        return (
            jsonify(
                {
                    "success": True,
                    "count": len(cleaned_data),
                    "data": cleaned_data.to_dict(orient="records"),
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


BASE_CURRENCY = os.getenv("BASE_CURRENCY")


@analytics_bp.route("/summary", methods=["GET"])
def analytics_summary():
    try:
        category = request.args.get("category")
        status = request.args.get("status")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        target_currency = request.args.get("currency", BASE_CURRENCY).upper()

        exchange_rate = get_exchange_rate(BASE_CURRENCY, target_currency)

        conn = get_db_connection()
        df = pd.read_sql("SELECT * FROM analytics_data", conn)
        if df.empty:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "No analytics data available. Upload files first.",
                    }
                ),
                400,
            )

        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

        if category and category != "All":
            df = df[df["category"].str.lower() == category.lower()]

        if status and status != "All":
            df = df[df["status"].str.lower() == status.lower()]

        if start_date:
            start = pd.to_datetime(start_date)
            df = df[df["order_date"] >= start]

        if end_date:
            end = pd.to_datetime(end_date)

            # Include the complete end date
            end = end + pd.Timedelta(days=1)

            df = df[df["order_date"] < end]

        if df.empty:
            return (
                jsonify(
                    {
                        "success": True,
                        "message": "No data found for the selected filters.",
                        "kpis": {
                            "total_revenue": 0,
                            "total_orders": 0,
                            "average_order_value": 0,
                        },
                        "revenue_trend": [],
                        "top_products": [],
                        "category_revenue": [],
                        "delivery_performance": {
                            "average_delivery_days": 0,
                            "status_counts": [],
                        },
                    }
                ),
                200,
            )

        total_revenue = df["revenue"].sum()
        converted_total_revenue = total_revenue * exchange_rate

        total_orders = df["order_id"].nunique()

        average_order_value = total_revenue / total_orders if total_orders > 0 else 0
        converted_average_order_value = average_order_value * exchange_rate

        revenue_trend = df.groupby("order_date")["revenue"].sum().reset_index()
        revenue_trend["revenue"] = revenue_trend["revenue"] * exchange_rate

        revenue_trend["order_date"] = revenue_trend["order_date"].dt.strftime(
            "%Y-%m-%d"
        )
        revenue_trend = revenue_trend.to_dict(orient="records")

        top_products = (
            df.groupby("product_name")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )
        top_products["revenue"] = top_products["revenue"] * exchange_rate
        top_products = top_products.to_dict(orient="records")

        category_revenue = df.groupby("category")["revenue"].sum().reset_index()
        category_revenue["revenue"] = category_revenue["revenue"] * exchange_rate
        category_revenue = category_revenue.to_dict(orient="records")

        average_delivery_days = df["delivery_days"].mean()
        delivery_status = df["status"].value_counts().reset_index()
        delivery_status.columns = ["status", "count"]

        delivery_status = delivery_status.to_dict(orient="records")
        return (
            jsonify(
                {
                    "success": True,
                    "currency": target_currency,
                    "exchange_rate": exchange_rate,
                    "kpis": {
                        "total_revenue": float(converted_total_revenue),
                        "total_orders": int(total_orders),
                        "average_order_value": float(converted_average_order_value),
                    },
                    "revenue_trend": revenue_trend,
                    "top_products": top_products,
                    "category_revenue": category_revenue,
                    "delivery_performance": {
                        "average_delivery_days": float(average_delivery_days),
                        "status_counts": delivery_status,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


# For testing purpose
# @analytics_bp.route("/api", methods=["GET"])
# def example():
#     data = get_exchange_rate("USD", "INR")

#     return {"status": True, "data": data}
