import os
from dotenv import load_dotenv
from authentication import Authentication
from cal import Calendar
from optimizer import Optimizer
from datetime import datetime, timedelta, timezone

## Load environment variables
load_dotenv()

# Create an Authentication object and build the service
auth = Authentication()
service = auth.build_service()

# Create a Calendar object
calendar_id = os.getenv('CALENDAR_ID')
print(calendar_id)
print(service)
calendar = Calendar(service, calendar_id)

# Get events for a specific time range
start_time = datetime.now()
end_time = start_time + timedelta(days=1)
events = calendar.get_events(start_time, end_time)

# Create an Optimizer object and optimize the events
optimizer = Optimizer(calendar)
events, gap = optimizer.check_overlaps(events)
optimizer.ensure_gaps(events, gap)

# Convert short events to tasks
optimizer.convert_short_events_to_tasks(events, end_time)

# Define the start and end times for the new event
start_time_event = datetime.now()
end_time_event = start_time_event + timedelta(hours=2)

# Define the summary and description for the new event
summary = 'My Event'
description = 'This is a description of my event.'

# Create the new event
new_event = calendar.create_event(start_time_event, end_time_event, summary, description)

# Delete the event
calendar.delete_event(new_event['id'])