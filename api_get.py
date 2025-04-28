from flask import Flask, request, jsonify
import joblib
import sqlite3
import uuid

app = Flask(__name__)
model = joblib.load('model.pkl')

# Admin secret (like your admin password)
ADMIN_SECRET = "Nikhil0007@"

# Connect to SQLite database
def connect_db():
    conn = sqlite3.connect('api_requests.db')
    return conn

# Initialize database
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            status TEXT,
            api_key TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return "🔵 ML Model API Backend is Running!"

@app.route('/request-api-key', methods=['POST'])
def request_api_key():
    data = request.get_json(force=True)
    username = data.get('username')

    if not username:
        return jsonify({"error": "Username is required"}), 400

    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM api_requests WHERE username = ?", (username,))
    if cursor.fetchone():
        return jsonify({"error": "Request already submitted or approved"}), 400

    cursor.execute("INSERT INTO api_requests (username, status) VALUES (?, ?)", (username, 'pending'))
    conn.commit()
    conn.close()

    return jsonify({"message": "Request submitted. Wait for admin approval."})

@app.route('/approve-api-key', methods=['POST'])
def approve_api_key():
    data = request.get_json(force=True)
    admin_secret = data.get('admin_secret')
    username = data.get('username')

    if admin_secret != ADMIN_SECRET:
        return jsonify({"error": "Unauthorized"}), 401

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM api_requests WHERE username = ? AND status = 'pending'", (username,))
    if not cursor.fetchone():
        return jsonify({"error": "No pending request for this username"}), 404

    api_key = str(uuid.uuid4())

    cursor.execute("UPDATE api_requests SET status = ?, api_key = ? WHERE username = ?", ('approved', api_key, username))
    conn.commit()
    conn.close()

    return jsonify({"username": username, "api_key": api_key})

@app.route('/predict', methods=['POST'])
def predict():
    api_key = request.headers.get('x-api-key')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM api_requests WHERE api_key = ? AND status = 'approved'", (api_key,))
    if not cursor.fetchone():
        return jsonify({"error": "Unauthorized or Invalid API Key"}), 401

    data = request.get_json(force=True)
    input_features = data['features']
    prediction = model.predict([input_features])

    return jsonify({'prediction': int(prediction[0])})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
