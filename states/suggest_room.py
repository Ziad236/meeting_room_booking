def run(state):
    # Suggest Room 3 as fallback
    if "error" in state:
        return {
            "room": "Room 3",
            "status": f"{state['room']} was unavailable. Suggested {state['room']} instead at {state['time']} on {state['day']}."
        }
    return state