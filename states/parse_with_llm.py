import json
from llm_agent import call_groq_llm

def run(state):
    user_input = state.get("request", "").strip()

    if not user_input:
        return {"error": "No user request provided."}

    system_prompt = """
You are a helpful assistant that extracts booking details from user input.

Your goal is to identify:
- Room number (e.g., Room 2)
- Day of the week (e.g., Monday)
- Time in 12-hour format with AM/PM (e.g., 3:00 PM)
- Number of persons

Respond in this exact JSON format:
{
  "room": "Room 2",
  "day": "monday",
  "time": "3:00 PM",
  "persons": 6
}

If any field is missing, set its value to null.
Only respond with valid JSON.
"""

    prompt = f"{system_prompt}\n\nUser input: {user_input}"

    try:
        response = call_groq_llm(prompt)
        parsed = json.loads(response)

        if not all([parsed.get("room"), parsed.get("day"), parsed.get("time"), parsed.get("persons")]):
            return {
                "error": "❌ Could not extract all booking details from your input. Please try rephrasing."
            }

        return {
            "room": parsed["room"],
            "day": parsed["day"].strip().lower(),
            "time": parsed["time"].strip(),
            "persons": int(parsed["persons"]),
            "parsed": True
        }

    except Exception as e:
        return {"error": f"LLM parsing failed: {str(e)}"}
