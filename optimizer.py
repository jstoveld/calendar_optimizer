from dateutil.parser import parse
from datetime import timedelta
from dateutil.tz import tzutc
from authentication import Authentication

class Optimizer:
    def __init__(self, calendar):
        self.calendar = calendar

    def convert_event_to_task(self, events):
        tasks = []
        remaining_events = []
        for event in events:
            # Ask the user if they want to convert the event to a task
            convert_to_task = input(f"Do you want to convert the event '{event['summary']}' to a task? (yes/no): ")
            if convert_to_task.lower() == 'yes':
                # Convert the start and end times to datetime objects
                start_time = parse(event['start'].get('dateTime', event['start'].get('date')))
                end_time = parse(event['end'].get('dateTime', event['end'].get('date')))
                # Convert the event to a task
                task = self.calendar.create_event(start_time, end_time, event['summary'], event.get('description'))
                tasks.append(task)
                # Update the event on the calendar
                self.calendar.update_event(event['id'], task)
            else:
                remaining_events.append(event)
        return tasks, remaining_events

    def optimize_events(self, events):
        # Implement your event optimization logic here
        # For example, you might want to sort the events by start time:
        events.sort(key=lambda x: x['start'].get('dateTime', x['start'].get('date')) if x['start'].get('dateTime', x['start'].get('date')) is not None else '')
        return events