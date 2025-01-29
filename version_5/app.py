from flask import Flask, request, jsonify, render_template
from transformers import pipeline

app = Flask(__name__)

# Load a pre-trained language model (e.g., GPT-2)
generator = pipeline('text-generation', model='gpt2')

# Route to serve the index.html file
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle autocomplete predictions
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    user_input = data['text']

    # Generate predictions with shorter and crisper outputs
    predictions = generator(
        user_input,
        max_length=20,  # Limit the length of the generated text
        num_return_sequences=3,  # Number of predictions to generate
        temperature=0.7,  # Lower temperature for more focused outputs
        top_k=50,  # Limit to top 50 likely next words
        top_p=0.9,  # Use nucleus sampling for better quality
        do_sample=True  # Enable sampling for more diverse outputs
    )

    # Extract the generated text
    results = [pred['generated_text'].strip() for pred in predictions]

    return jsonify({'predictions': results})

if __name__ == '__main__':
    app.run(debug=True)