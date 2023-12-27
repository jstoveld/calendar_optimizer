import os
from dotenv import load_dotenv
from authentication import Authentication
from cal import Calendar
from optimizer import Optimizer
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Create an Authentication object and build the service
auth = Authentication()
service = auth.build_service()

# Create a Calendar object
calendar_id = os.getenv('CALENDAR_ID')
calendar = Calendar(service, calendar_id)

# Get events for a specific time range
start_time = datetime.now()
end_time = start_time + timedelta(days=1)
events = calendar.get_events(start_time, end_time)

# Create an Optimizer object
optimizer = Optimizer(calendar)

# Check for overlapping events
overlapping_events, gap = optimizer.check_overlaps(events)
if overlapping_events:
    print("The following events overlap:")
    for overlap_group in overlapping_events:
        for event in overlap_group:
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            end_time = event['end'].get('dateTime', event['end'].get('date'))
            print(f"- {event['summary']} from {start_time} to {end_time}")
else:
    print("No overlapping events found.")

try:
    # Ask the user if they want to optimize their calendar
    user_input = input("Do you want to optimize your calendar? (yes/no): ")
    if user_input.lower() == 'yes':
        tasks_to_convert = []

        # Iterate through the events
        for event in events:
            # Ask the user if the event should be converted to a task
            user_input = input(f"Do you want to convert the event '{event['summary']}' to a task? (yes/no): ")
            if user_input.lower() == 'yes':
                # Store the event for later conversion
                tasks_to_convert.append(event)
            else:
                # Ask the user if the event is longer than it should be
                user_input = input(f"Is the event '{event['summary']}' longer than it should be? (yes/no): ")
                if user_input.lower() == 'yes':
                    # Ask the user for the desired duration of the event
                    while True:
                        try:
                            duration = int(input("Please enter the desired duration of the event in minutes (30 or 60): "))
                            break
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                    # Adjust the duration of the event
                    optimizer.adjust_event_duration(event, duration)

        # Convert the selected events to tasks
        events_copy = events.copy()
        for task in tasks_to_convert:
            optimizer.convert_event_to_task(task, events_copy)
        events = events_copy

        # Check for overlapping events
        overlapping_events, gap = optimizer.check_overlaps(events)

        # If there are overlapping events
        if overlapping_events:
            # Ask the user if they want to mark them for requiring attention
            user_input = input("There are overlapping events. Do you want to mark them for requiring attention? (yes/no): ")
            if user_input.lower() == 'yes':
                # Mark the overlapping events for requiring attention
                optimizer.mark_events_for_attention(overlapping_events)

        print("Your calendar has been optimized.")
    else:
        print("No changes have been made to your calendar.")

    # Convert short events to tasks
    calendar.convert_short_events_to_tasks(events)

    # Get the updated events from the calendar
    updated_events = calendar.get_events(start_time, end_time)

    # Check if any events were converted to tasks
    if len(events) != len(updated_events):
        print("Some events were converted to tasks.")
    else:
        print("No events were converted to tasks.")
except Exception as e:
    print(f"An error occurred: {e}")