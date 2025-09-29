import requests
import json
from flask import Flask, request, jsonify

# --- Configuration ---
app = Flask(__name__)
URL = "https://westeros.famapp.in/txn/create/payout/add/"

# ⚠️ REPLACE WITH YOUR ACTUAL TOKEN (It is highly recommended to use environment variables for tokens)
AUTH_TOKEN = "eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiZXBrIjp7Imt0eSI6Ik9LUCIsImNydiI6Ilg0NDgiLCJ4IjoicGEwWmVNd255eFBKYXB5ZU9ud>"

HEADERS = {
    "User-Agent": "A015 | Android 15 | Dalvik/2.1.0 | Tetris | 318D0D6589676E17F88CCE03A86C2591C8EBAFBA | 3.11.5 (Build>",
    "Accept-Encoding": "gzip",
    "Content-Type": "application/json; charset=UTF-8",
    "x-device-details": "A015 | Android 15 | Dalvik/2.1.0 | Tetris | 318D0D6589676E17F88CCE03A86C2591C8EBAFBA | 3.11.5 >",
    "x-app-version": "525",
    "x-platform": "1",
    "device-id": "290db21f38c0907b",
    "authorization": f"Token {AUTH_TOKEN}"
}

def check_fam_upi(upi_id):
    """Function to make the API request."""
    data = {
        "upi_string": f"upi://pay?pa={upi_id}",
        "init_mode": "00",
        "is_uploaded_from_gallery": False
    }
    
    try:
        response = requests.post(URL, headers=HEADERS, json=data, timeout=10)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API Request Failed: {e}"}
    except json.JSONDecodeError:
        return {"error": "Received non-JSON or malformed response from external API."}

@app.route('/check_upi', methods=['POST'])
def check_upi_endpoint():
    """Endpoint to accept UPI ID and return JSON response."""
    
    # Expect the request to have a JSON body with the 'upi_id' key
    request_data = request.get_json(silent=True)
    
    if not request_data or 'upi_id' not in request_data:
        return jsonify({"error": "Invalid request. Expected JSON body with 'upi_id' key."}), 400
    
    upi_id = request_data['upi_id'].strip()
    
    if not upi_id:
        return jsonify({"error": "UPI ID cannot be empty."}), 400
        
    # Get the response from the external API
    result = check_fam_upi(upi_id)
    
    # Return the result as JSON
    if "error" in result:
         # Return a 500 status code if the external API failed
        return jsonify(result), 500
    else:
        # Return the successful data with a 200 status code
        return jsonify(result)

@app.route('/', methods=['GET'])
def instructions():
    """Simple root endpoint to explain how to use the API."""
    return jsonify({
        "status": "Service Running",
        "instructions": "To use this API, send a POST request to /check_upi with a JSON body.",
        "example_body": {"upi_id": "tanveer297@fam"}
    })

if __name__ == '__main__':
    # Use a specific port for local testing
    app.run(host='0.0.0.0', port=5000, debug=True)
      
