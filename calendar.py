class Calendar:
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