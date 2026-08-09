from flask import Blueprint, jsonify, request
import pandas as pd
from parser import parse_json, parse_csv, parse_xml
from services import flatten_orders, parse_shipments, merge_data, clean_data
from data.store import storedata
from database import get_db_connection

ingest_bp = Blueprint("ingest", __name__, url_prefix="/ingest")


# ONE ROUTE FOR ALL THE FILES
@ingest_bp.route("/upload", methods=["POST"])
def upload_files():
    orders_file = request.files.get("orders")
    products_file = request.files.get("products")
    shipments_file = request.files.get("shipments")

    if not orders_file or not products_file or not shipments_file:
        return (
            jsonify({"success": False, "message": "All three files are required"}),
            400,
        )

    try:
        orders_json = parse_json(orders_file)
        orders_data = flatten_orders(orders_json)
        orders_df = pd.DataFrame(orders_data)

        products_df = parse_csv(products_file)

        shipments_root = parse_xml(shipments_file)
        shipments_data = parse_shipments(shipments_root)
        shipments_df = pd.DataFrame(shipments_data)

        merged_data = merge_data(orders_df, products_df, shipments_df)
        cleaned_data = clean_data(merged_data)

        conn = get_db_connection()
        cleaned_data.to_sql("analytics_data", conn, if_exists="replace", index=False)

        return (
            jsonify(
                {
                    "success": True,
                    "data": cleaned_data.to_dict(orient="records"),
                    "message": "Merged And Cleaned Data",
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


# ROUTE FOR JSON FILE
@ingest_bp.route("/json", methods=["POST"])
def ingest_json():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files.get("file")

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if not file.filename.endswith(".json"):
            return (
                jsonify({"success": False, "message": "Only JSON files are allowed"}),
                400,
            )

        data = parse_json(file)
        flattend_data = flatten_orders(data)

        # storedata["orders"] = pd.DataFrame(flattend_data)

        orders_df = pd.DataFrame(flattend_data)
        conn = get_db_connection()
        orders_df.to_sql("orders", conn, if_exists="replace", index=False)
        conn.close()

        return (
            jsonify(
                {
                    "success": True,
                    "data": flattend_data,
                    "message": "JSON ingestion API",
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


# ROUTE FOR CSV FILE
@ingest_bp.route("/csv", methods=["POST"])
def ingest_csv():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files.get("file")

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if not file.filename.endswith(".csv"):
            return (
                jsonify({"success": False, "message": "Only CSV files are allowed"}),
                400,
            )

        products_df = parse_csv(file)
        # storedata["products"] = data

        conn = get_db_connection()
        products_df.to_sql("products", conn, if_exists="replace", index=False)

        conn.close()

        return jsonify(
            {
                "succes": True,
                "data": products_df.to_dict(orient="records"),
                "message": "CSV ingestion API",
            }
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


# ROUTE FOR XML FILE
@ingest_bp.route("/xml", methods=["POST"])
def ingest_xml():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files.get("file")

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if not file.filename.endswith(".xml"):
            return (
                jsonify({"success": False, "message": "Only XML files are allowed"}),
                400,
            )
        root = parse_xml(file)
        data = parse_shipments(root)

        # storedata["shipments"] = pd.DataFrame(data)
        shipments_df = pd.DataFrame(data)
        conn = get_db_connection()
        shipments_df.to_sql("shipments", conn, if_exists="replace", index=False)
        conn.close()

        return jsonify({"succes": True, "data": data, "message": "XML ingestion API"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
