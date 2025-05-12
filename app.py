"""
Streamlit UI for the Meeting Room Booking Assistant.

This application allows users to:
- Submit natural-language room booking requests
- View assistant suggestions powered by an LLM via LangGraph
- Automatically confirm bookings and create Google Calendar events
- View all existing bookings in a live table

Requires a valid Groq API key and authorized Google Calendar access.
"""
import streamlit as st
from datetime import datetime, timedelta, timezone
from graph import run_graph
from services.room_service import get_all_bookings
from calendar_utils import get_calendar_service, check_availability, create_event

st.set_page_config(page_title="Meeting Room Booking Assistant")
st.title("Meeting Room Booking Assistant")

for key in ["result", "room", "day", "time", "persons", "calendar_event_link"]:
    if key not in st.session_state:
        st.session_state[key] = None

user_input = st.text_input(
    "Request a room booking (e.g. 'reserve room 2 at 3:00 PM on Monday for 6 persons')"
)

if st.button("Submit"):
    if user_input:
        result = run_graph(user_input)
        st.session_state.result = result
        st.session_state.calendar_event_link = None

        if isinstance(result, dict):
            for key in ["room", "day", "time", "persons", "suggested_room", "suggested_day", "suggested_time"]:
                st.session_state[key] = result.get(key)

            room = result.get("suggested_room") or result.get("room")
            day = result.get("suggested_day") or result.get("day")
            time = result.get("suggested_time") or result.get("time")

            if result.get("confirmed") and all([room, day, time]):
                try:
                    service = get_calendar_service()

                    parsed_time = datetime.strptime(time.strip().lower(), "%I:%M %p")
                    now = datetime.now(timezone.utc)
                    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                    today_index = now.weekday()
                    target_index = days.index(day.lower())
                    delta_days = (target_index - today_index) % 7
                    target_date = now + timedelta(days=delta_days)

                    start_time = target_date.replace(
                        hour=parsed_time.hour,
                        minute=parsed_time.minute,
                        second=0,
                        microsecond=0,
                    )
                    end_time = start_time + timedelta(hours=1)

                    busy_slots = check_availability(service, start_time, end_time)
                    if result.get("user_busy"):
                        st.warning("⚠️ Your calendar shows you're busy at this time. Booking was still attempted.")
                    else:
                        event = create_event(
                            service,
                            summary=f"{room} Booking",
                            start_time=start_time,
                            end_time=end_time,
                            location=room,
                            description="Auto-booked via LangGraph AI agent"
                        )
                        st.session_state.calendar_event_link = event.get('htmlLink')
                except Exception as e:
                    st.error(f"Google Calendar integration failed: {e}")
    else:
        st.warning("Please enter a booking request.")

if st.session_state.result:
    result = st.session_state.result
    if isinstance(result, dict):
        message = (
            result.get("llm_response")
            or result.get("error")
            or result.get("status")
        )
    else:
        message = result

    st.markdown("#### Assistant Response")
    st.info(message)

    if result.get("booking_confirmed") and st.session_state.calendar_event_link:
        st.success("📅 Booking added to your calendar!")
        st.markdown(f"[View on Google Calendar]({st.session_state.calendar_event_link})")

        st.markdown("---")
        st.subheader("📋 Current Bookings")

        bookings = get_all_bookings()
        if bookings:
            st.dataframe(bookings, use_container_width=True)
        else:
            st.info("No bookings found yet.")
    else:
        st.info("ℹ️ No confirmed bookings to show.")

st.markdown("---")
st.subheader("📋 Current Bookings")

bookings = get_all_bookings()
if bookings:
    st.dataframe(bookings, use_container_width=True)
else:
    st.info("No bookings found yet.")
