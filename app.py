import os
from dotenv import load_dotenv
from authentication import Authentication
from cal import Calendar
from optimizer import Optimizer
from task import Task
from converter import Converter
from datetime import datetime, timedelta
from googleapiclient.errors import HttpError

# Load environment variables
load_dotenv()

# Create an Authentication object and build the service
auth = Authentication()
service = auth.build_service()

# Create a Calendar object
calendar_id = os.getenv('CALENDAR_ID')
calendar = Calendar(service, calendar_id)

# Create a Task object and select a tasklist
tasks_service = auth.build_tasks_service()
task = Task(tasks_service)
selected_tasklist_id = task.select_tasklist()

try:
    # Get events for a specific time range
    start_time = datetime.now()
    end_time = start_time + timedelta(days=1)
    events = calendar.get_events(start_time, end_time)
except HttpError as e:
    if e.resp.status == 400:
        # Delete the token.pickle file
        if os.path.exists('token.pickle'):
            os.remove('token.pickle')
        # Renew the token and rebuild the service
        auth.renew_token()
        service = auth.build_service()
        # Recreate the Calendar object with the new service
        calendar = Calendar(service, calendar_id)
        # Retry getting the events
        events = calendar.get_events(start_time, end_time)
    else:
        raise

# Create a Converter object
converter = Converter(calendar, task)

# Get tasks from the selected tasklist
tasks = task.get_tasks(selected_tasklist_id)

# Convert events to tasks based on user input and get the remaining events
tasks, events = converter.event_to_task(events)



# Convert tasks to events based on user input
events = converter.task_to_event(tasks)

# Create an Optimizer object
optimizer = Optimizer(calendar)
overlapping_event_groups = optimizer.identify_overlapping_events(events)
optimizer.handle_overlapping_events(overlapping_event_groups)










    # # Optimize the remaining events
    # optimized_events = optimizer.optimize_events(events)

    # # Print tasks
    # print("Tasks:")
    # for task in tasks:
    #     print(f"Summary: {task['summary']}")
    #     print(f"Start: {task['start'].get('dateTime', task['start'].get('date'))}")
    #     print(f"End: {task['end'].get('dateTime', task['end'].get('date'))}")
    #     print()

    # # Print optimized events
    # print("Optimized events:")
    # for event in optimized_events:
    #     print(f"Summary: {event['summary']}")
    #     print(f"Start: {event['start'].get('dateTime', event['start'].get('date'))}")
    #     print(f"End: {event['end'].get('dateTime', event['end'].get('date'))}")
    #     print()