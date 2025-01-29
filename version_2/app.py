from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Your Hugging Face API Key
HUGGING_FACE_API_KEY = 'YOUR HUGGING FACE API KEY'  # Replace with your actual API key

# Route to serve the HTML file
@app.route('/')
def home():
    return render_template('index.html')

# Endpoint to get predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        prompt = data['prompt']
        
        # Make API call to Hugging Face for sentence completion
        headers = {
            "Authorization": f"Bearer {HUGGING_FACE_API_KEY}"
        }
        payload = {
            "inputs": prompt,
            "options": {"use_cache": False}
        }
        
        response = requests.post(
            'https://api-inference.huggingface.co/models/distilgpt2',
            headers=headers,
            json=payload
        )
        
        # Check if the response is successful
        if response.status_code == 200:
            response_data = response.json()
            
            # Extract the generated text from the response (which is a list of dictionaries)
            if isinstance(response_data, list) and len(response_data) > 0:
                generated_text = response_data[0].get('generated_text', '')
                return jsonify({'predictions': [generated_text]})
            else:
                return jsonify({'error': 'No predictions found in the response'}), 500
        else:
            # Log the error for debugging
            print(f"Error from Hugging Face API: {response.status_code}, {response.text}")
            return jsonify({'error': 'Error in prediction', 'details': response.text}), 500

    except Exception as e:
        # Log any unexpected errors
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)