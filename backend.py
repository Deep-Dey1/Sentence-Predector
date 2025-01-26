from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to ["http://127.0.0.1:5500"] if using Live Server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load pretrained model for text generation
generator = pipeline("text-generation", model="gpt2")

# Define request model
class InputText(BaseModel):
    text: str

@app.post("/predict")
def predict(input_text: InputText):
    prompt = input_text.text
    output = generator(prompt, max_length=50, num_return_sequences=1)
    return {"prediction": output[0]["generated_text"]}

# Restart backend after this change!
