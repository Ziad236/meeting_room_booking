import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_FILE = 'your_token'
CREDENTIALS_FILE = 'your_credentials'


def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=8080)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def check_availability(service, start_time, end_time):
    """
    Checks if the user's calendar is busy between start_time and end_time.

    Args:
        service: Google Calendar API service object
        start_time (datetime): timezone-aware start datetime
        end_time (datetime): timezone-aware end datetime

    Returns:
        list: List of busy time blocks (empty if free)
    """
    body = {
        "timeMin": start_time.isoformat(),  # no 'Z'
        "timeMax": end_time.isoformat(),
        "timeZone": "UTC",
        "items": [{"id": "primary"}]
    }

    try:
        events_result = service.freebusy().query(body=body).execute()
        return events_result['calendars']['primary']['busy']
    except Exception as e:
        print("❌ Google Calendar freebusy query failed:", e)
        return [{"error": str(e)}]


def create_event(service, summary, start_time, end_time, location=None, description=None):
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'UTC'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'UTC'},
    }
    return service.events().insert(calendarId='primary', body=event).execute()
