from calendar import Calendar

## TODO: Implement the Optimizer class

class Optimizer:
    def __init__(self, calendar):
        self.calendar = calendar

    def check_overlaps(self, events):
        # Check for overlapping events and ask the user to approve them
        pass

    def ensure_gaps(self, events):
        # Ensure there is a 5-10 minute gap between each event
        pass

    def convert_short_events_to_tasks(self, events):
        # Convert events that are less than 15 minutes long to tasks
        for event in events:
            self.calendar.convert_event_to_task(event)

    def calculate_travel_time(self, events):
        # Calculate the travel time between events
        pass