from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import pytz,dateutil.parser, os
from dateutil.parser import parse
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



## Find out if events are too long or too short for the intended action
## TODO Bake in the ability to change the expected duration of each event
def analyze_events(events, expected_duration):
    too_short_events = []
    too_long_events = []
    right_duration_events = []

    for event in events:
        start = parse(event['start'].get('dateTime', event['start'].get('date')))
        end = parse(event['end'].get('dateTime', event['end'].get('date')))
        if start.tzinfo is None or start.tzinfo.utcoffset(start) is None:
            start = start.replace(tzinfo=pytz.UTC)
        if end.tzinfo is None or end.tzinfo.utcoffset(end) is None:
            end = end.replace(tzinfo=pytz.UTC)
        duration = end - start
        if 'hour' in event.get('description', ''):
            expected_duration = timedelta(hours=1)

        if expected_duration is not None:
            if duration < expected_duration:
                too_short_events.append(event)
            elif duration > expected_duration:
                too_long_events.append(event)
            else:
                right_duration_events.append(event)
    print(f'You have {len(too_short_events)} calendar events that are too short.')
    print(f'You have {len(too_long_events)} calendar events that are too long.')
    print(f'You have {len(right_duration_events)} calendar events with the right duration.')
    return too_short_events, too_long_events, right_duration_events

def analyze_start_times(events):
    morning = 0
    afternoon = 0
    evening = 0

    for event in events:
        start = parse(event['start'].get('dateTime', event['start'].get('date')))
        if start.tzinfo is None or start.tzinfo.utcoffset(start) is None:
            start = start.replace(tzinfo=pytz.UTC)
        if start.hour < 12:
            morning += 1
        elif start.hour < 18:
            afternoon += 1
        else:
            evening += 1

    print(f'You have {morning} events in the morning, {afternoon} events in the afternoon, and {evening} events in the evening.')
analyze_start_times(events)

def meeting_overlap(events):
    # First, ask the user about each event and modify the end time
    for i in range(len(events)):
        all_day = input(f"Is the event '{events[i]['summary']}' an all-day event? (yes/no) ")
        if all_day.lower() == 'no':
            duration = input("How long should this event be? 15, 30, or 60 minutes? ")
            while duration not in ['15', '30', '60']:
                print("Invalid input. Please enter 15, 30, or 60.")
                duration = input("How long should this event be? 15, 30, or 60 minutes? ")
            duration = timedelta(minutes=int(duration))
            start_i = parse(events[i]['start'].get('dateTime', events[i]['start'].get('date')))
            events[i]['end']['dateTime'] = (start_i + duration).isoformat()

    # Then, compare each event with every other event to check for overlaps
    overlap = False
    overlapping_events = []
    checked_pairs = set()
    for i in range(len(events)):
        for j in range(i + 1, len(events)):
            if (i, j) in checked_pairs or (j, i) in checked_pairs:
                continue
            checked_pairs.add((i, j))
            start_i = events[i]['start'].get('dateTime', events[i]['start'].get('date'))
            end_i = events[i]['end'].get('dateTime', events[i]['end'].get('date'))
            start_j = events[j]['start'].get('dateTime', events[j]['start'].get('date'))
            end_j = events[j]['end'].get('dateTime', events[j]['end'].get('date'))

            if start_i and end_i and start_j and end_j:
                if start_i < end_j and end_i > start_j:
                    overlap = True
                    overlapping_events.append(events[i]['summary'])  # Only append the title of the event

    if overlap:
        print('You have overlapping events tomorrow:')
        for event in overlapping_events:
            start_time = events[i]['start'].get('dateTime', events[i]['start'].get('date'))
            end_time = events[i]['end'].get('dateTime', events[i]['end'].get('date'))
            print(f'Event: {event}, Start time: {start_time}, End time: {end_time}')
    else:
        print('You have no overlapping events tomorrow.')

meeting_overlap(events)
