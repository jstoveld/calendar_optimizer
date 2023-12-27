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

# Ask the user if they want to optimize their calendar
user_input = input("Do you want to optimize your calendar? (yes/no): ")
if user_input.lower() == 'yes':
    events, gap = optimizer.optimize_events(events)
    optimizer.ensure_gaps(events, gap)
    optimizer.convert_short_events_to_tasks(events, end_time)
    print("Your calendar has been optimized.")
else:
    print("No changes have been made to your calendar.")