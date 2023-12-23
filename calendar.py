class Calendar:
    def __init__(self, service, calendar_id):
        self.service = service
        self.calendar_id = calendar_id

    def get_events(self, start_time, end_time):
        events_result = self.service.events().list(
            calendarId=self.calendar_id, 
            timeMin=start_time.isoformat(), 
            timeMax=end_time.isoformat(), 
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

    def convert_event_to_task(self, event_id, task_title, task_notes=None):
        # Delete the event
        self.delete_event(event_id)

        # Create a new task
        task = {
            'title': task_title,
            'notes': task_notes,
            # Add any other necessary task properties here
        }
        task = self.service.tasks().insert(tasklist='@default', body=task).execute()
        return task