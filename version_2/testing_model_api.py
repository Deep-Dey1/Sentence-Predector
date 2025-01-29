import requests

# Define the Hugging Face API URL for distilgpt2 model
url = "https://api-inference.huggingface.co/models/distilgpt2"

# Replace 'your_access_token' with your actual Hugging Face access token
headers = {
    "Authorization": "Bearer Huggin face api"
}

# Define your input prompt
data = {
    "inputs": "Once upon a time"
}

# Send POST request to the API
response = requests.post(url, headers=headers, json=data)

# Check the response status
if response.status_code == 200:
    # Parse the response and print the generated text
    result = response.json()
    print("Generated Text: ", result[0]["generated_text"])
else:
    print(f"Error: {response.status_code}")
    print(response.json())
