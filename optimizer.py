from dateutil.parser import parse
from datetime import timedelta
from dateutil.tz import tzutc
from authentication import Authentication
from datetime import datetime
from dateutil.tz import tzlocal


class Optimizer:
    def __init__(self, calendar):
        self.calendar = calendar

    def get_event_start_time(self, event):
        # Get the start time of the event
        start_time = parse(event['start'].get('dateTime', event['start'].get('date')))

        # If the start time is offset-naive, make it offset-aware by adding the local timezone
        if start_time.tzinfo is None or start_time.tzinfo.utcoffset(start_time) is None:
            start_time = start_time.replace(tzinfo=tzlocal())

        return start_time

    def get_event_end_time(self, event):
        # Get the end time of the event
        end_time = parse(event['end'].get('dateTime', event['end'].get('date')))

        # If the end time is offset-naive, make it offset-aware by adding the local timezone
        if end_time.tzinfo is None or end_time.tzinfo.utcoffset(end_time) is None:
            end_time = end_time.replace(tzinfo=tzlocal())

        return end_time

    def identify_overlapping_events(self, events):
        # Sort the events by start time
        events.sort(key=self.get_event_start_time)

        overlapping_event_groups = []
        current_group = [events[0]]
        for i in range(1, len(events)):
            # If the start time of the current event is before the end time of the last event in the current group, they overlap
            if self.get_event_start_time(events[i]) < self.get_event_end_time(current_group[-1]):
                # Add the current event to the current group
                current_group.append(events[i])
            else:
                # If the current group has more than one event, it's an overlapping group
                if len(current_group) > 1:
                    overlapping_event_groups.append(current_group)
                # Start a new group with the current event
                current_group = [events[i]]

        # Don't forget to add the last group if it's an overlapping group
        if len(current_group) > 1:
            overlapping_event_groups.append(current_group)

        if overlapping_event_groups:
            print("The following calendar events have a clash:")
            for group in overlapping_event_groups:
                print(", ".join(event['summary'] for event in group))
        else:
            print("No overlapping events found.")

        return overlapping_event_groups
    
    def handle_overlapping_events(self, overlapping_event_groups):
        for group in overlapping_event_groups:
            print(f"The following events overlap: {', '.join(event['summary'] for event in group)}")
            print("What would you like to do?")
            print("1. Delete an event")
            print("2. Reschedule an event")
            print("3. Shorten an event")
            print("4. Ignore the overlap")
            choice = input("Enter the number of your choice: ")

            if choice == '1':
                for i, event in enumerate(group):
                    print(f"{i+1}. {event['summary']}")
                event_to_delete = input("Enter the number of the event you want to delete: ")
                # Delete the selected event...
                # TODO: Delete the selected event
            elif choice == '2':
                for i, event in enumerate(group):
                    print(f"{i+1}. {event['summary']}")
                event_to_reschedule = input("Enter the number of the event you want to reschedule: ")
                # Reschedule the selected event...
                # TODO: Reschedule the selected event
            elif choice == '3':
                for i, event in enumerate(group):
                    print(f"{i+1}. {event['summary']}")
                event_to_shorten = input("Enter the number of the event you want to shorten: ")
                # Shorten the selected event...
                # TODO: Shorten the selected event
            elif choice == '4':
                # Ignore the overlap
                pass
            else:
                print("Invalid choice. Please try again.")