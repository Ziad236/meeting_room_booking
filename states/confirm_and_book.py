from services.room_service import add_booking

def run(state):
    if state.get("confirmed") or state["request"].lower().strip() in ["yes", "confirm", "confirm booking"]:
        booked = add_booking(state["room"], state["day"], state["time"])
        if booked:
            return {"status": f"✅ Booking confirmed for {state['room']} at {state['time']} on {state['day']}."}
        else:
            return {"error": "❌ Failed to confirm booking. Room might already be booked."}
    return {"status": "Waiting for user confirmation..."}
