from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load pre-trained model and tokenizer
model_name = "distilgpt2"  # You can use any other model if needed
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def autocomplete(input_text, max_length=50, temperature=0.7, stop_token="."):
    # Encode the input text to tensor
    inputs = tokenizer.encode(input_text, return_tensors="pt")
    
    # Generate the model's prediction
    outputs = model.generate(inputs, max_length=len(inputs[0]) + max_length, temperature=temperature, 
                             pad_token_id=tokenizer.eos_token_id, 
                             do_sample=True, 
                             top_k=50, 
                             top_p=0.95,
                             eos_token_id=tokenizer.encode(stop_token)[0])
    
    # Decode the output tensor to string
    prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Return the prediction after the input text
    return prediction[len(input_text):]

# Main Loop for Web-like Behavior
if __name__ == "__main__":
    print("Welcome to the autocomplete system! Type 'exit' to quit.")
    
    while True:
        # User input
        user_input = input("Start typing a sentence: ")
        
        if user_input.lower() == "exit":
            break
        
        # Get prediction from model
        predicted_text = autocomplete(user_input)
        
        # Output predicted text
        print(f"Autocompleted text: {predicted_text}")
