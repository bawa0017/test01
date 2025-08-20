import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
# Enable CORS for all routes and all origins (good for dev/testing)
CORS(app, resources={r"/*": {"origins": "*"}})

# Connect to MongoDB using environment variable
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    raise ValueError("MONGO_URI environment variable not set")

client = MongoClient(mongo_uri)
db = client["admin"]  # Database name

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    name = data.get('name')
    age = data.get('age')

    if not name or not age:
        return jsonify({"error": "Name and age are required"}), 400

    # Insert into MongoDB
    db.users.insert_one({"name": name, "age": age})

    return jsonify({
        "message": f"Hello, {name}! You are {age} years old."
    }), 200

# Optional: health check endpoint for Kubernetes
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    # Host 0.0.0.0 so it works inside Docker/K8s
    app.run(debug=True, host='0.0.0.0', port=5001)

