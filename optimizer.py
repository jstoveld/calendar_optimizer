from calendar import Calendar
from datetime import timedelta

class Optimizer:
    def __init__(self, calendar):
        self.calendar = calendar

    def check_overlaps(self, start_time, end_time):
        # Get all events between start_time and end_time
        events = self.calendar.get_events(start_time, end_time)

        # Sort events by start time
        events.sort(key=lambda x: x['start']['dateTime'])

        # Check for overlapping events
        for i in range(1, len(events)):
            if events[i]['start']['dateTime'] < events[i-1]['end']['dateTime']:
                print(f"Overlapping events: {events[i-1]['summary']} and {events[i]['summary']}")

    def ensure_gaps(self, start_time, end_time):
        # Get all events between start_time and end_time
        events = self.calendar.get_events(start_time, end_time)

        # Ensure there is a 5-10 minute gap between each event
        for i in range(1, len(events)):
            gap = events[i]['start']['dateTime'] - events[i-1]['end']['dateTime']
            if gap < timedelta(minutes=5) or gap > timedelta(minutes=10):
                print(f"Inadequate gap between {events[i-1]['summary']} and {events[i]['summary']}")

    def convert_short_events_to_tasks(self, start_time, end_time):
        # Get all events between start_time and end_time
        events = self.calendar.get_events(start_time, end_time)

        # Convert short events to tasks
        for event in events:
            self.calendar.convert_event_to_task(event)

    def calculate_travel_time(self, start_time, end_time):
        # Get all events between start_time and end_time
        events = self.calendar.get_events(start_time, end_time)

        # Calculate travel time between events
        for i in range(1, len(events)):
            travel_time = events[i]['start']['dateTime'] - events[i-1]['end']['dateTime']
            if travel_time < timedelta(minutes=15):  # less than 15 minutes
                print(f"Not enough travel time between {events[i-1]['summary']} and {events[i]['summary']}")