from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Private EC2 backend IP
PRIVATE_BACKEND = "http://10.0.131.64:5000/api/order"  # Replace with your private EC2 IP

@app.route("/api/order", methods=["POST"])
def proxy_order():
    try:
        data = request.json
        res = requests.post(PRIVATE_BACKEND, json=data, timeout=5)
        res.raise_for_status()
        return jsonify(res.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to reach private backend", "details": str(e)}), 502
    except ValueError:
        return jsonify({"error": "Private backend returned invalid JSON"}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
