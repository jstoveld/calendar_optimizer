from cal import Calendar
from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil.tz import tzutc

class Optimizer:
    def __init__(self, calendar):
        self.calendar = calendar

    def check_overlaps(self, events):
        # Sort events by start time
        events.sort(key=lambda x: x['start'].get('dateTime', x['start'].get('date')))

        # Check for overlaps and calculate gap
        gap = None
        for i in range(1, len(events)):
            start_i = parse(events[i]['start'].get('dateTime', events[i]['start'].get('date'))).astimezone(tzutc())
            end_i_1 = parse(events[i-1]['end'].get('dateTime', events[i-1]['end'].get('date'))).astimezone(tzutc())
            if start_i < end_i_1:
                print(f"Overlap between {events[i-1]['summary']} and {events[i]['summary']}")
            else:
                gap = (start_i - end_i_1).total_seconds() / 60  # Calculate gap in minutes

        # Return the sorted list of events and the gap
        return events, gap

    def ensure_gaps(self, events, gap):
        # Check if gap is less than 5 minutes
        if gap < 5:
            print(f"Insufficient gap of {gap} minutes")

    def convert_short_events_to_tasks(self, events, end_time):
        for event in events:
            start_time = parse(event['start'].get('dateTime', event['start'].get('date'))).astimezone(tzutc())
            end_event_time = parse(event['end'].get('dateTime', event['end'].get('date'))).astimezone(tzutc())
            duration = (end_event_time - start_time).total_seconds() / 60  # Calculate duration in minutes
            if duration < 30:  # If the event is shorter than 30 minutes
                self.calendar.delete_event(event['id'])
                self.calendar.create_task(event['summary'], event['description'])

    def calculate_travel_time(self, start_time, end_time):
        # Get all events between start_time and end_time
        events = self.calendar.get_events(start_time, end_time)

        # Calculate travel time between events
        for i in range(1, len(events)):
            travel_time = events[i]['start']['dateTime'] - events[i-1]['end']['dateTime']
            if travel_time < timedelta(minutes=15):  # less than 15 minutes
                print(f"Not enough travel time between {events[i-1]['summary']} and {events[i]['summary']}")