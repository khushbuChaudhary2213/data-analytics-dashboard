from flask import Blueprint, jsonify, request
import pandas as pd
import os
from parser import parse_json, parse_csv, parse_xml
from services import flatten_orders, parse_shipments, merge_data, clean_data
from database import get_db_connection

ingest_bp = Blueprint("ingest", __name__, url_prefix="/ingest")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")


# ONE ROUTE FOR ALL THE FILES
@ingest_bp.route("/upload", methods=["POST"])
def upload_files():
    orders_upload = request.files.get("orders")
    products_upload = request.files.get("products")
    shipments_upload = request.files.get("shipments")

    # If files are uploaded, use them
    if orders_upload and products_upload and shipments_upload:
        orders_file = orders_upload
        products_file = products_upload
        shipments_file = shipments_upload

    else:
        orders_file = os.path.join(data_dir, "orders.json")
        products_file = os.path.join(data_dir, "products.csv")
        shipments_file = os.path.join(data_dir, "shipments.xml")

    try:
        engine = get_db_connection()

        orders_json = parse_json(orders_file)
        orders_data = flatten_orders(orders_json)
        orders_df = pd.DataFrame(orders_data)
        orders_df.to_sql("orders", engine, if_exists="replace", index=False)

        products_df = parse_csv(products_file)
        products_df.to_sql("products", engine, if_exists="replace", index=False)

        shipments_root = parse_xml(shipments_file)
        shipments_data = parse_shipments(shipments_root)
        shipments_df = pd.DataFrame(shipments_data)
        shipments_df.to_sql("shipments", engine, if_exists="replace", index=False)

        merged_data = merge_data(orders_df, products_df, shipments_df)
        cleaned_data = clean_data(merged_data)

        cleaned_data.to_sql("analytics_data", engine, if_exists="replace", index=False)

        return (
            jsonify(
                {
                    "success": True,
                    "data": cleaned_data.to_dict(orient="records"),
                    "message": "Files processed and data stored successfully.",
                }
            ),
            200,
        )
    except Exception as e:
        print("UPLOAD ERROR:", e)

        return (
            jsonify(
                {"success": False, "message": "Failed to process the uploaded files."}
            ),
            500,
        )


# ROUTE FOR JSON FILE
@ingest_bp.route("/json", methods=["POST"])
def ingest_json():
    try:
        if "file" in request.files:
            file = request.files.get("file")
        else:
            file = os.path.join(data_dir, "orders.json")

        data = parse_json(file)
        flattend_data = flatten_orders(data)

        # storedata["orders"] = pd.DataFrame(flattend_data)

        orders_df = pd.DataFrame(flattend_data)
        engine = get_db_connection()
        orders_df.to_sql("orders", engine, if_exists="replace", index=False)

        return (
            jsonify(
                {
                    "success": True,
                    "data": flattend_data,
                    "message": "JSON data processed successfully.",
                }
            ),
            200,
        )
    except Exception as e:
        print("JSON INGESTION ERROR:", e)

        return (
            jsonify({"success": False, "message": "Failed to process JSON file."}),
            500,
        )


# ROUTE FOR CSV FILE
@ingest_bp.route("/csv", methods=["POST"])
def ingest_csv():
    try:
        if "file" in request.files:
            file = request.files.get("file")
        else:
            file = os.path.join(data_dir, "products.csv")

        products_df = parse_csv(file)
        # storedata["products"] = data

        engine = get_db_connection()
        products_df.to_sql("products", engine, if_exists="replace", index=False)

        return (
            jsonify(
                {
                    "success": True,
                    "data": products_df.to_dict(orient="records"),
                    "message": "CSV data processed successfully.",
                }
            ),
            200,
        )
    except Exception as e:
        print("CSV INGESTION ERROR:", e)

        return (
            jsonify({"success": False, "message": "Failed to process CSV file."}),
            500,
        )


# ROUTE FOR XML FILE
@ingest_bp.route("/xml", methods=["POST"])
def ingest_xml():
    try:
        if "file" in request.files:
            file = request.files.get("file")
        else:
            file = os.path.join(data_dir, "shipments.xml")

        root = parse_xml(file)
        data = parse_shipments(root)

        # storedata["shipments"] = pd.DataFrame(data)
        shipments_df = pd.DataFrame(data)
        engine = get_db_connection()
        shipments_df.to_sql("shipments", engine, if_exists="append", index=False)

        return (
            jsonify(
                {
                    "success": True,
                    "data": data,
                    "message": "XML data processed successfully.",
                }
            ),
            200,
        )
    except Exception as e:
        print("XML INGESTION ERROR:", e)

        return (
            jsonify({"success": False, "message": "Failed to process XML file."}),
            500,
        )
