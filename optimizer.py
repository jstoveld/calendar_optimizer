from dateutil.parser import parse
from datetime import timedelta
from dateutil.tz import tzutc
from authentication import Authentication
from datetime import datetime


class Optimizer:
    def __init__(self, calendar):
        self.calendar = calendar

    @staticmethod
    def get_event_start_time(event):
        """Extract and parse the start time of an event"""
        start_time_str = event['start'].get('dateTime', event['start'].get('date'))
        start_time = parse(start_time_str)

        # If the start time is offset-naive, make it offset-aware by adding the UTC timezone
        if start_time.tzinfo is None or start_time.tzinfo.utcoffset(start_time) is None:
            start_time = start_time.replace(tzinfo=tzutc())

        return start_time

    @staticmethod
    def get_event_end_time(event):
        """Extract and parse the end time of an event"""
        end_time_str = event['end'].get('dateTime', event['end'].get('date'))
        end_time = parse(end_time_str)

        # If the end time is offset-naive, make it offset-aware by adding the UTC timezone
        if end_time.tzinfo is None or end_time.tzinfo.utcoffset(end_time) is None:
            end_time = end_time.replace(tzinfo=tzutc())

        return end_time

    def identify_overlapping_events(self, events):
        # Sort the events by start time
        events.sort(key=self.get_event_start_time)

        overlapping_events = []
        for i in range(1, len(events)):
            # If the start time of the current event is before the end time of the previous event, they overlap
            if self.get_event_start_time(events[i]) < self.get_event_end_time(events[i-1]):
                overlapping_events.append((events[i-1], events[i]))

        if overlapping_events:
            print("The following calendar events have a clash:")
            for event1, event2 in overlapping_events:
                print(f"\"{event1['summary']}\" overlaps with \"{event2['summary']}\"")
        else:
            print("No overlapping events found.")

        return overlapping_events










## Will Revisit
    # def optimize_events(self, events):
    #     # Implement your event optimization logic here
    #     # For example, you might want to sort the events by start time:
    #     events.sort(key=lambda x: x['start'].get('dateTime', x['start'].get('date')) if x['start'].get('dateTime', x['start'].get('date')) is not None else '')
    #     return events