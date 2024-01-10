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
    
    #TODO This is broken because the dateTime is posting a KeyError.
    def find_open_blocks(self, events):
        """
        Find open blocks of time in a calendar.

        Parameters:
        events (list): The list of events. Each event is a dictionary with 'start' and 'end' keys.

        Returns:
        list: A list of open blocks. Each block is a dictionary with 'start' and 'end' keys.
        """
        # Convert the 'dateTime' strings into datetime objects and sort the events by start time
        for event in events:
            event['start'] = datetime.fromisoformat(event['start']['dateTime'])
            event['end'] = datetime.fromisoformat(event['end']['dateTime'])
        events.sort(key=lambda event: event['start'])

        open_blocks = []
        for i in range(1, len(events)):
            # If the gap between the end of the previous event and the start of the current event is greater than min_duration...
            if events[i]['start'] - events[i-1]['end'] >= self.min_duration:
                # ...then this is an open block
                open_blocks.append({'start': events[i-1]['end'], 'end': events[i]['start']})

        return open_blocks
    
    ##########################################################
    
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
                event_id_to_delete = group[int(event_to_delete) - 1]['id']  # Assuming 'id' is a key in your event dictionary
                self.calendar.delete_event(event_id_to_delete)
                print(f"Event {event_to_delete} has been deleted.")
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