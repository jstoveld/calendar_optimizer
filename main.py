from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta
import dateutil.parser

# Load credentials and create a service
flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', ['https://www.googleapis.com/auth/calendar'])
credentials = flow.run_local_server(port=0)
service = build('calendar', 'v3', credentials=credentials)

def get_events(service, calendar_id='primary', time_min=None, time_max=None):
    now =datetime.now()

    time_min = datetime(now.year, now.month, now.day) + timedelta(days=1)
    time_max = time_min + timedelta(days=1)

    ## Convert datetime to RFC3339 format required by API
    time_min = time_min.isoformat()
    time_max = time_max.isoformat()

    ## Call the API
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    ## Get all events
    events = events_result.get('items', [])
    print(events)

    return events

# Call the get_events function
events = get_events(service)









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
