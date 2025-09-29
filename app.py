import requests
import json
from flask import Flask, request, jsonify

# --- 1. Configuration ---
app = Flask(__name__)
URL = "https://westeros.famapp.in/txn/create/payout/add/"

# ⚠️ REPLACE WITH YOUR ACTUAL TOKEN
# NOTE: For production, use environment variables (os.environ.get('AUTH_TOKEN'))
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

# --- 2. Core API Logic ---
def check_fam_upi(upi_id):
    """Function to make the external API request."""
    data = {
        "upi_string": f"upi://pay?pa={upi_id}",
        "init_mode": "00",
        "is_uploaded_from_gallery": False
    }
    
    try:
        # Use POST for the external API call
        response = requests.post(URL, headers=HEADERS, json=data, timeout=10)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API Request Failed: {e}"}
    except json.JSONDecodeError:
        return {"error": "Received non-JSON or malformed response from external API."}

# --- 3. Flask Endpoint (Accessible via Browser GET) ---
@app.route('/', methods=['GET'])
def check_upi_browser_view():
    """
    Endpoint to check UPI ID via a GET request using a query parameter.
    Example URL: https://your-service-name.onrender.com/?upi_id=tanveer297@fam
    """
    # Get UPI ID from URL query parameters (e.g., ?upi_id=...)
    upi_id = request.args.get('upi_id', '').strip()

    if not upi_id:
        # Instructions if no upi_id is provided
        return jsonify({
            "status": "Instructions",
            "message": "To check a UPI ID, append it as a query parameter to the URL.",
            "example_access": "https://your-service-name.onrender.com/?upi_id=tanveer297@fam"
        })

    # Get the response from the external API
    result = check_fam_upi(upi_id)

    # Return the result as JSON (browsers will format this automatically)
    if "error" in result:
        # Use a client error status code for clarity, though 200 is often fine for JSON
        return jsonify(result), 400
    else:
        return jsonify(result)

# --- 4. Local Run Command ---
if __name__ == '__main__':
    # Use a specific port for local testing
    app.run(host='0.0.0.0', port=5000, debug=True)
                                 
