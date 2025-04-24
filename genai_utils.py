
import google.generativeai as genai  # Import Google Gemini API

# Function to count tokens using Gemini API
def count_tokens(text):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.count_tokens(text)
    return response.total_tokens
