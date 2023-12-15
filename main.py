from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import pytz,dateutil.parser, os
import pickle
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
calendar_id = os.getenv('CALENDAR_ID')

# Load credentials from file, if it exists
credentials = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)

# If there are no (valid) credentials available, let the user log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', ['https://www.googleapis.com/auth/calendar'])
        credentials = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(credentials, token)

# Create a service
service = build('calendar', 'v3', credentials=credentials)

def get_events(service, calendar_id=calendar_id):
    # Get the current date and time
    now = datetime.now(pytz.utc)

    # Set time_min as the start of tomorrow
    time_min = datetime(now.year, now.month, now.day, tzinfo=pytz.utc) + timedelta(days=1)

    # Set time_max as the end of tomorrow
    time_max = time_min + timedelta(days=1)

    # Convert datetime objects to RFC3339 format
    time_min = time_min.isoformat()
    time_max = time_max.isoformat()

    # Call the Google Calendar API
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    # Get the list of events
    events = events_result.get('items', [])

    return events

# Call the get_events function
events = get_events(service)


# How Many Events Do You Have Tomorrow?
event_count=0
if events != []:
    for event in events:
        event_count=event_count+1
print(f'You have {event_count} events tomorrow.')










## TODO

# def analyze_events(events):
#     # Analyze events and find optimization opportunities
#     pass

# def create_event(service, calendar_id='primary', event_data=None):
#     # Create a new event or update an existing one
#     pass

# # Get events
# events = get_events(service)

# # Analyze and optimize
# optimized_events = analyze_events(events)

# # Create or update events
# for event in optimized_events:
#     create_event(service, event_data=event)
