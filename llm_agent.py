import requests

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = "enter_gorq_key"


def call_groq_llm(prompt: str) -> str:
    """
    Sends a prompt to the Groq-hosted LLaMA 3.1 8B language model and returns the assistant's response.

    The function makes a POST request to the Groq API with the specified prompt,
    using the `llama3-8b-8192` model and a system message suited for a meeting room booking assistant.

    Args:
        prompt (str): The user's input or query to be passed to the LLM.

    Returns:
        str: The LLM-generated response as a string.

    Raises:
        HTTPError: If the request to the Groq API fails (non-2xx status).
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful meeting room booking assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
