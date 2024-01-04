from dateutil.parser import parse
from datetime import datetime

class Converter:
    def __init__(self, calendar, task):
        self.calendar = calendar
        self.task = task


## Handles the tasks created from events.
    def event_to_task(self, events):
        tasks = []
        remaining_events = []
        for event in events:
            convert_to_task = input(f"Do you want to convert the event '{event['summary']}' to a task? (yes/no): ")
            if convert_to_task.lower() == 'yes':
                start_time = parse(event['start'].get('dateTime', event['start'].get('date')))
                end_time = parse(event['end'].get('dateTime', event['end'].get('date')))

                if not isinstance(end_time, datetime):
                    print(f"Error: Could not parse the end time of the event '{event['summary']}'. Skipping this event.")
                    continue

                title = event['summary']
                notes = event.get('description', '')

                task = self.task.create_task(title, notes, end_time)
                tasks.append(task)

                self.calendar.delete_event(event['id'])
                print(f"The event '{event['summary']}' has been converted to a task and deleted from the calendar.")
            else:
                remaining_events.append(event)
        return tasks, remaining_events

    def task_to_event(self, tasks):
        events = []
        for task in tasks:
            convert_to_event = input(f"Does the task '{task['title']}' require an event on our calendar? (yes/no): ")
            if convert_to_event.lower() == 'yes':
                title = task['title']

                event = self.calendar.create_event(title)
                events.append(event)

                self.task.delete_task(task['id'])
                print(f"The task '{task['title']}' has been converted to an event and deleted from the task list.")
        return events