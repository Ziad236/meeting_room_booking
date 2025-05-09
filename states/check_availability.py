def run(state):
    # Placeholder logic: assume room is available
    if state.get("parsed"):
        return {
            "status": f"{state['room']} is available at {state['time']} on {state['day']} for {state['persons']} persons."
        }
    return {"error": "Input parsing failed."}