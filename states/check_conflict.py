def run(state):
    # Placeholder conflict logic
    if state.get("room") == "Room 2" and state.get("time") == "3:00 PM":
        return {"error": f"{state['room']} is already booked at {state['time']} on {state['day']}."}
    return state