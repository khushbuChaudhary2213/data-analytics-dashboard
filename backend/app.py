from flask import Flask, jsonify
from routes.ingest import ingest_bp
from routes.analytics import analytics_bp

app = Flask(__name__)

app.register_blueprint(ingest_bp)
app.register_blueprint(analytics_bp)


@app.route("/")
def home():
    return jsonify({"message": "Analytics Dashboard API is running"})


if __name__ == "__main__":
    app.run(debug=True)
