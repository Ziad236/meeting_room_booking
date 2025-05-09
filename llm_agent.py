import requests
import os

#GROQ_API_KEY = os.getenv("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")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = "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"

def call_groq_llm(messages, model="llama-3.1-8b-instant"):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print("❌ Error:", response.status_code)
        print("Response:", response.text)

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
