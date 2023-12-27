from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil.tz import tzutc
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

    def create_event(self, start_time, end_time, summary, description=None):
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
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