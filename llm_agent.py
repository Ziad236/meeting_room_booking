import requests
import os


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = "enter_groq_api_key"

def call_groq_llm(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "llama3-8b-8192",  # or the model you're using
        "messages": [
            {"role": "system", "content": "You are a helpful meeting room booking assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
