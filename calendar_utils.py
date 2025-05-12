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
    body = {
        "timeMin": start_time.isoformat() + 'Z',
        "timeMax": end_time.isoformat() + 'Z',
        "items": [{"id": "primary"}]
    }
    events_result = service.freebusy().query(body=body).execute()
    return events_result['calendars']['primary']['busy']


def create_event(service, summary, start_time, end_time, location=None, description=None):
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'UTC'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'UTC'},
    }
    return service.events().insert(calendarId='primary', body=event).execute()
