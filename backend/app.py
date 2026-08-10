from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from routes.ingest import ingest_bp
from routes.analytics import analytics_bp
from database import init_db

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")

app = Flask(__name__)
init_db()
CORS(app, origins=[FRONTEND_URL])

app.register_blueprint(ingest_bp)
app.register_blueprint(analytics_bp)


@app.route("/")
def home():
    return jsonify({"message": "Analytics Dashboard API is running"})


if __name__ == "__main__":
    app.run(debug=True)
