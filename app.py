import streamlit as st
from graph import run_graph
from services.room_service import get_all_bookings

st.set_page_config(page_title="Meeting Room Booking Assistant")
st.title("Meeting Room Booking Assistant")

# Initialize session state
for key in ["result", "room", "day", "time", "persons"]:
    if key not in st.session_state:
        st.session_state[key] = None

# User input
user_input = st.text_input(
    "Request a room booking (e.g. 'reserve room 2 at 3:00 PM on Monday for 6 persons')"
)

# Submit booking request
if st.button("Submit"):
    if user_input:
        # Run graph and get full state result
        result = run_graph(user_input)
        st.session_state.result = result

        # Extract room info into session state
        if isinstance(result, dict):
            for key in ["room", "day", "time", "persons"]:
                st.session_state[key] = result.get(key)
    else:
        st.warning("Please enter a booking request.")

# Show assistant response
if st.session_state.result:
    result = st.session_state.result

    if isinstance(result, dict):
        message = result.get("llm_response") or result.get("status") or result.get("error")
    else:
        message = result

    st.markdown("#### Assistant Response")
    st.info(message)

# Show current bookings
st.markdown("---")
st.subheader("📋 Current Bookings")

bookings = get_all_bookings()
if bookings:
    st.dataframe(bookings, use_container_width=True)
else:
    st.info("No bookings found yet.")
