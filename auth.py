import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Define the scope for Google Calendar access
SCOPES = ['https://www.googleapis.com/auth/calendar']

def generate_token():
    creds = None

    # Run OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=8080)

    # Save the token as token.pkl
    with open("token.pkl", "wb") as token_file:
        pickle.dump(creds, token_file)

    print("✅ token.pkl generated successfully!")

if __name__ == "__main__":
    generate_token()
