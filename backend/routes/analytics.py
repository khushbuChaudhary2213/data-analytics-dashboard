from flask import Blueprint, jsonify
from data.store import storedata
from services import merge_data, clean_data

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")


@analytics_bp.route("/data", methods=["GET"])
def analytics_data():

    if (
        storedata["orders"] is None
        or storedata["products"] is None
        or storedata["shipments"] is None
    ):
        return (
            jsonify(
                {"success": False, "message": "Please upload all three files first"}
            ),
            400,
        )

    merged_data = merge_data(
        storedata["orders"], storedata["products"], storedata["shipments"]
    )
    cleaned_data = clean_data(merged_data)
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


@analytics_bp.route("/summary", methods=["GET"])
def analytics_summary():
    if (
        storedata["orders"] is None
        or storedata["products"] is None
        or storedata["shipments"] is None
    ):
        return (
            jsonify(
                {"success": False, "message": "Please upload all three files first"}
            ),
            400,
        )
    merged_data = merge_data(
        storedata["orders"], storedata["products"], storedata["shipments"]
    )

    df = clean_data(merged_data)

    total_revenue = df["revenue"].sum()

    total_orders = df["order_id"].nunique()

    average_order_value = total_revenue / total_orders if total_orders > 0 else 0

    revenue_trend = df.groupby("order_date")["revenue"].sum().reset_index()
    revenue_trend["order_date"] = revenue_trend["order_date"].dt.strftime("%Y-%m-%d")
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
