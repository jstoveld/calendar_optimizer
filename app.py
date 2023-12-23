from authentication import Authentication
from calendar import Calendar
from optimizer import Optimizer
from datetime import datetime, timedelta

# Create an Authentication object and build the service
auth = Authentication()
service = auth.build_service()

# Create a Calendar object
calendar_id = 'your-calendar-id'
calendar = Calendar(service, calendar_id)

# Get events for a specific time range
start_time = datetime.now()
end_time = start_time + timedelta(days=1)
events = calendar.get_events(start_time, end_time)

# Create an Optimizer object and optimize the events
optimizer = Optimizer(calendar)
optimizer.check_overlaps(events)
optimizer.ensure_gaps(events)
optimizer.convert_short_events_to_tasks(events)
# optimizer.calculate_travel_time(events)  # Uncomment this line if you implement this method

# Create a new event
start_time = datetime.now()
end_time = start_time + timedelta(hours=1)
summary = 'My Event'
description = 'This is a description of my event.'
new_event = calendar.create_event(start_time, end_time, summary, description)

# Delete the event
calendar.delete_event(new_event['id'])