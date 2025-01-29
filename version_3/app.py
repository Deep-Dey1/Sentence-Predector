from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Correct API URL and key
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
API_KEY = "YOUR GEMINI API KEY"  # Replace with your actual Gemini API Key

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if "prompt" not in data:
            return jsonify({"error": "Missing 'prompt' in request"}), 400

        prompt = data["prompt"]

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        headers = {
            "Content-Type": "application/json"
        }

        # Send request to Gemini API
        response = requests.post(f"{GEMINI_API_URL}?key={API_KEY}", json=payload, headers=headers)

        # Print response status and raw content for debugging
        print("Status Code:", response.status_code)
        print("Raw Response Text:", response.text)

        if response.status_code == 404:
            return jsonify({"error": "API endpoint not found. Check the URL."}), 404

        if not response.text:
            return jsonify({"error": "Empty response from Gemini API"}), 500

        response_data = response.json()  # Convert to JSON
        candidates = response_data.get("candidates", [])
        if candidates:
            predictions = candidates[0].get("content", "No prediction available")
        else:
            predictions = "No prediction available"

        return jsonify({"prediction": predictions})

    except requests.exceptions.RequestException as e:
        print("Request Error:", str(e))
        return jsonify({"error": "Request to Gemini API failed"}), 500

    except Exception as e:
        print("Server Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
