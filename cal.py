from datetime import datetime, timedelta, time
from dateutil.parser import parse
from dateutil.tz import tzutc
from tzlocal import get_localzone
from zoneinfo import ZoneInfo
from authentication import Authentication


class Calendar:
    def __init__(self, service, calendar_id):
        self.service = service
        self.calendar_id = calendar_id

    def get_events(self, start_time, end_time):
        events_result = self.service.events().list(
            calendarId=self.calendar_id, 
            timeMin=start_time.isoformat() + 'Z', 
            timeMax=end_time.isoformat() + 'Z', 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return events_result.get('items', [])

    def create_event(self, title, start_time=None, end_time=None, description=None):
        # Get the local timezone
        local_tz = get_localzone()

        # If start_time is not provided, set it to 10am the next day
        if start_time is None:
            now = datetime.now(local_tz)
            start_time = datetime(now.year, now.month, now.day, 10, 0, 0, tzinfo=local_tz) + timedelta(days=1)

        # If end_time is not provided, set it to 1 hour after the start_time
        if end_time is None:
            end_time = start_time + timedelta(hours=1)

        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': str(local_tz),
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': str(local_tz),
            },
        }
        created_event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
        return created_event

    def delete_event(self, event_id):
        self.service.events().delete(calendarId=self.calendar_id, eventId=event_id).execute()

    def update_event(self, event_id, event):
        # Fetch the current event from the server
        current_event = self.service.events().get(calendarId=self.calendar_id, eventId=event_id).execute()
        # Set the sequence value in the update request to the current sequence value
        event['sequence'] = current_event['sequence']
        # Update the event
        updated_event = self.service.events().update(calendarId=self.calendar_id, eventId=event_id, body=event).execute()
        return updated_event

    def create_task(self, summary, description=None, start_time=None, end_time=None):
        if start_time is None:
            start_time = datetime.now(tzutc())
            end_time = start_time + timedelta(hours=1)  # Set the duration of the task to 1 hour

        task = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'America/New_York',
            },
            'transparency': 'transparent',  # This makes the task "free" rather than "busy"
        }

        task = self.service.events().insert(calendarId=self.calendar_id, body=task).execute()
        return task