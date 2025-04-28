import requests
import time
import sqlite3
import uuid

# Admin secret for approval (same as in your previous setup)
ADMIN_SECRET = "Nikhil0007@"

# Function to check if the user exists in the database and is waiting for approval
def check_user_request(username):
    conn = sqlite3.connect('api_requests.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests WHERE username = ? AND status = 'pending'", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Function to approve the API key for the user
def approve_user_request(username):
    conn = sqlite3.connect('api_requests.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE requests SET status = 'approved' WHERE username = ?", (username,))
    conn.commit()

    # Generate a new API key
    api_key = str(uuid.uuid4())
    
    # Save the API key to the database
    cursor.execute("UPDATE requests SET api_key = ? WHERE username = ?", (api_key, username))
    conn.commit()
    conn.close()

    return api_key

# Function to simulate making a prediction with the generated API key
def make_prediction(api_key):
    url = "http://127.0.0.1:5000/predict"
    headers = {"x-api-key": api_key}
    data = {"features": [5.1, 3.5, 1.4, 0.2]}  # Example input features

    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error while making API request: {e}")
        return None

# Automation Pipeline
def automation_pipeline(username):
    # Step 1: Check if the user exists and is pending approval
    print("Step 1: Checking user request...")
    user = check_user_request(username)
    if not user:
        print(f"User {username} does not exist or is not pending approval.")
        return

    print(f"Step 2: Approving request for {username}...")
    api_key = approve_user_request(username)
    print(f"User {username} approved! API key generated: {api_key}")

    # Step 3: Make the prediction request using the generated API key
    print("Step 3: Triggering prediction using the API key...")
    prediction_result = make_prediction(api_key)
    
    if prediction_result:
        print(f"Prediction result: {prediction_result}")
    else:
        print("Prediction failed.")

# Main execution
if __name__ == "__main__":
    # Example: The username to be processed
    username_to_process = "niksss"
    automation_pipeline(username_to_process)
