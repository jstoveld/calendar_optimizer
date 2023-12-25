from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil.tz import tzutc


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
                'dateTime': start_time.isoformat() + 'Z',
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': end_time.isoformat() + 'Z',
                'timeZone': 'America/New_York',
            },
        }
        event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
        return event
    
    def delete_event(self, event_id):
        self.service.events().delete(calendarId=self.calendar_id, eventId=event_id).execute()

    def convert_short_events_to_tasks(self, events, end_time):
        for event in events:
            start_time = parse(event['start'].get('dateTime', event['start'].get('date'))).astimezone(tzutc())
            end_event_time = parse(event['end'].get('dateTime', event['end'].get('date'))).astimezone(tzutc())
            duration = (end_event_time - start_time).total_seconds() / 60  # Calculate duration in minutes
            if duration < 30:  # If the event is shorter than 30 minutes
                self.calendar.delete_event(event['id'])
                self.calendar.create_task(event['summary'], event['description'])