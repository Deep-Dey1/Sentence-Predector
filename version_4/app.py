from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Correct API URL and key (Replace with your actual Gemini API Key)
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
API_KEY = "YOUR GEMINI API KEY" 

@app.route("/")
def home():
    """Renders the HTML template for the user interface."""
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    """Handles POST requests to predict sentence completions."""
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

        response = requests.post(f"{GEMINI_API_URL}?key={API_KEY}", json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes

        response_data = response.json()
        candidates = response_data.get("candidates", [])

        if candidates:
            prediction = candidates[0]["content"]["parts"][0]["text"]
        else:
            prediction = "No prediction available"

        return jsonify({"prediction": prediction})

    except requests.exceptions.RequestException as e:
        print("Request Error:", str(e))
        return jsonify({"error": "Request to Gemini API failed"}), 500

    except Exception as e:
        print("Server Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)