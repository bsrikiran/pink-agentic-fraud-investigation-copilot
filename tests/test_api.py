import os
from dotenv import load_dotenv
from openai import OpenAI

# Load the hidden .env file
load_dotenv()

# Initialize client (automatically pulls OPENAI_API_KEY from environment)
client = OpenAI()

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Respond with the word 'Connected!'"}]
    )
    print(f"Result: {response.choices[0].message.content}")
except Exception as e:
    print(f"Error connecting to OpenAI: {e}")
