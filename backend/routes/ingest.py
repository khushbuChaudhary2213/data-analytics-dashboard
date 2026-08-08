from flask import Blueprint, jsonify, request
import pandas as pd
from parser import parse_json, parse_csv, parse_xml
from services import flatten_orders, parse_shipments
from data.store import storedata

ingest_bp = Blueprint("ingest", __name__, url_prefix="/ingest")


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

        storedata["orders"] = pd.DataFrame(flattend_data)
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

        data = parse_csv(file)
        storedata["products"] = data

        return jsonify(
            {
                "succes": True,
                "data": data.to_dict(orient="records"),
                "message": "CSV ingestion API",
            }
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


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

        storedata["shipments"] = pd.DataFrame(data)
        return jsonify({"succes": True, "data": data, "message": "XML ingestion API"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
