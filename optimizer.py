from cal import Calendar
from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil.tz import tzutc

class Optimizer:
    def __init__(self, calendar):
        self.calendar = calendar

    def convert_event_to_task(self, event, events):
        # Convert the event to a task
        task = {
            'summary': event['summary'],
            'start': event['start'],
            'end': event['end'],
            'description': event.get('description', ''),
            'location': event.get('location', ''),
            'status': 'task'
        }
        # Remove the event from the list of events
        events.remove(event)
        return task

    def optimize_events(self, events):
        # Implement your event optimization logic here
        # For example, you might want to sort the events by start time:
        events.sort(key=lambda x: x['start'].get('dateTime', x['start'].get('date')))

        # Calculate the gap between events
        gap = None
        for i in range(1, len(events)):
            start_i = parse(events[i]['start'].get('dateTime', events[i]['start'].get('date'))).astimezone(tzutc())
            end_i_1 = parse(events[i-1]['end'].get('dateTime', events[i-1]['end'].get('date'))).astimezone(tzutc())
            gap = (start_i - end_i_1).total_seconds() / 60  # Calculate gap in minutes

        # Return the optimized events and the gap
        return events, gap

    def check_overlaps(self, events):
        # Sort events by start time
        events.sort(key=lambda x: x['start'].get('dateTime', x['start'].get('date')))

        # Check for overlaps and calculate gap
        overlapping_events = []
        gap = None
        for i in range(1, len(events)):
            start_i = parse(events[i]['start'].get('dateTime', events[i]['start'].get('date'))).astimezone(tzutc())
            end_i_1 = parse(events[i-1]['end'].get('dateTime', events[i-1]['end'].get('date'))).astimezone(tzutc())
            if start_i < end_i_1:
                overlapping_events.append([events[i-1], events[i]])
            gap = (start_i - end_i_1).total_seconds() / 60  # Calculate gap in minutes

        # Return the overlapping events and the gap
        return overlapping_events, gap

    def ensure_gaps(self, events, gap):
        # Adjust events to ensure a gap of at least 5 minutes
        for i in range(1, len(events)):
            start_i = parse(events[i]['start'].get('dateTime', events[i]['start'].get('date'))).astimezone(tzutc())
            end_i_1 = parse(events[i-1]['end'].get('dateTime', events[i-1]['end'].get('date'))).astimezone(tzutc())
            if (start_i - end_i_1).total_seconds() / 60 < gap:
                # Adjust the start time of the current event
                events[i]['start']['dateTime'] = (end_i_1 + timedelta(minutes=gap)).isoformat()

    def convert_short_events_to_tasks(self, events, end_time):
        tasks = []
        for event in events:
            start_time = parse(event['start'].get('dateTime', event['start'].get('date'))).astimezone(tzutc())
            end_time = parse(event['end'].get('dateTime', event['end'].get('date'))).astimezone(tzutc())
            duration = (end_time - start_time).total_seconds() / 60  # Calculate duration in minutes
            if duration <= 30:
                # Convert the event to a task
                tasks.append(event)
                events.remove(event)
        return tasks, events

    def calculate_travel_time(self, start_time, end_time):
        # Get all events between start_time and end_time and sort them by start time
        events = sorted(self.calendar.get_events(start_time, end_time), key=lambda x: x['start'].get('dateTime', x['start'].get('date')))

        # Calculate travel time between events
        for i in range(1, len(events)):
            travel_time = parse(events[i]['start'].get('dateTime', events[i]['start'].get('date'))).astimezone(tzutc()) - parse(events[i-1]['end'].get('dateTime', events[i-1]['end'].get('date'))).astimezone(tzutc())
            if travel_time < timedelta(minutes=15):  # less than 15 minutes
                print(f"Not enough travel time between {events[i-1]['summary']} and {events[i]['summary']}")
    
    def adjust_event_duration(self, event, duration):
        # Parse the start time of the event
        start_time = parse(event['start'].get('dateTime', event['start'].get('date'))).astimezone(tzutc())
        # Calculate the new end time based on the desired duration
        end_time = start_time + timedelta(minutes=duration)
        # Update the end time of the event
        if 'dateTime' in event['end']:
            event['end']['dateTime'] = end_time.isoformat()
        else:
            event['end']['date'] = end_time.date().isoformat()


    def identify_short_events(self, events):
        short_events = []
        for event in events:
            start_time = parse(event['start'].get('dateTime', event['start'].get('date'))).astimezone(tzutc())
            end_time = parse(event['end'].get('dateTime', event['end'].get('date'))).astimezone(tzutc())
            duration = (end_time - start_time).total_seconds() / 60  # Calculate duration in minutes
            if duration <= 30:
                # Add the event to the list of short events
                short_events.append(event)
        return short_events
    
    