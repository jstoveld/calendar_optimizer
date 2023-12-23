class Event:
    def __init__(self, service, calendar_id):
        self.service = service
        self.calendar_id = calendar_id

    def create_event(self, start_time, end_time, summary, description=None):
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
        }
        event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
        return event

    def delete_event(self, event_id):
        self.service.events().delete(calendarId=self.calendar_id, eventId=event_id).execute()

    def update_event(self, event_id, start_time=None, end_time=None, summary=None, description=None):
        event = self.service.events().get(calendarId=self.calendar_id, eventId=event_id).execute()

        if summary:
            event['summary'] = summary
        if description:
            event['description'] = description
        if start_time:
            event['start']['dateTime'] = start_time.isoformat()
        if end_time:
            event['end']['dateTime'] = end_time.isoformat()

        updated_event = self.service.events().update(calendarId=self.calendar_id, eventId=event_id, body=event).execute()
        return updated_event