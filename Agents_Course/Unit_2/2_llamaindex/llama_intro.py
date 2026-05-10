from llama_index.llms.google_genai import GoogleGenAI
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Retrieve HF_TOKEN from the environment variables
gemini_token = os.getenv("GEMINI_KEY")

llm = GoogleGenAI(
    model="models/gemini-3.1-flash-lite",
    temperature=0.7,
    max_tokens=100,
    api_key=gemini_token
)

response = llm.complete("Hello, how are you?")
print(response)