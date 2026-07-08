from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQUEST_COUNT = Counter('flask_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('flask_request_latency_seconds', 'Request latency', ['endpoint'])

@app.before_request
def before_request():
    pass

@app.route("/")
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    return "Hello from Flask behind nginx!"

@app.route("/health")
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health').inc()
    return jsonify({"status": "ok"})

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)