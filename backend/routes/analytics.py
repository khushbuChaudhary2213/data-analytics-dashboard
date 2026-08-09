from flask import Blueprint, jsonify
from data.store import storedata
from services import merge_data, clean_data, get_country_currency
from database import get_db_connection
import pandas as pd

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")


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


@analytics_bp.route("/summary", methods=["GET"])
def analytics_summary():
    try:
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

        total_revenue = df["revenue"].sum()

        total_orders = df["order_id"].nunique()

        average_order_value = total_revenue / total_orders if total_orders > 0 else 0

        revenue_trend = df.groupby("order_date")["revenue"].sum().reset_index()
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
        top_products = top_products.to_dict(orient="records")

        category_revenue = df.groupby("category")["revenue"].sum().reset_index()
        category_revenue = category_revenue.to_dict(orient="records")

        average_delivery_days = df["delivery_days"].mean()
        delivery_status = df["status"].value_counts().reset_index()
        delivery_status.columns = ["status", "count"]

        delivery_status = delivery_status.to_dict(orient="records")
        return (
            jsonify(
                {
                    "success": True,
                    "kpis": {
                        "total_revenue": float(total_revenue),
                        "total_orders": int(total_orders),
                        "average_order_value": float(average_order_value),
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
#     data = get_country_currency("India")

#     return {"status": True, "data": data}
