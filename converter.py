from dateutil.parser import parse

class Converter:
    def __init__(self, calendar, task):
        self.calendar = calendar
        self.task = task


## TODO We need to revise this so that the method will not reply with an error on notes. 
## Likely an issue with converiting the desctiption to notes - or a None object.
    def event_to_task(self, events):
        tasks = []
        remaining_events = []
        for event in events:
            # Ask the user if they want to convert the event to a task
            convert_to_task = input(f"Do you want to convert the event '{event['summary']}' to a task? (yes/no): ")
            if convert_to_task.lower() == 'yes':
                # Convert the start and end times to datetime objects
                start_time = parse(event['start'].get('dateTime', event['start'].get('date')))
                end_time = parse(event['end'].get('dateTime', event['end'].get('date')))
                
                # Map event fields to task fields
                title = event['summary']
                notes = event.get('description', '')  # provide a default value of '' for description
                due_date = end_time  # or start_time, depending on your needs
                
                # Convert the event to a task
                task = self.task.create_task(title, notes, due_date)
                tasks.append(task)
                
                # Delete the event from the calendar
                self.calendar.delete_event(event['id'])
                print(f"The event '{event['summary']}' has been converted to a task and deleted from the calendar.")
            else:
                remaining_events.append(event)
        return tasks, remaining_events
    
    def task_to_event(self, task):
        # Convert the task to a calendar event
        # Use self.calendar to interact with the calendar
        pass
