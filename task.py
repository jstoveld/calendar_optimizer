class Task:
    def __init__(self, service, tasklist_name='@default'):
        self.service = service
        self.tasklist_id = self.get_tasklist_id(tasklist_name)

    def get_tasklist_id(self, tasklist_name):
        """Get the ID of the task list with the specified name"""
        # Get the list of task lists
        tasklists = self.service.tasklists().list().execute()

        # Find the task list with the specified name
        for tasklist in tasklists['items']:
            if tasklist['title'] == tasklist_name:
                return tasklist['id']

        # If no task list with the specified name is found, return '@default'
        return '@default'

    def create_task(self, title, notes, due_date=None):
        """Create a new task in the specified task list"""
        # Define the task
        task = {
            'title': title,
            'notes': notes,
        }
        if due_date:
            task['due'] = due_date.isoformat()+'Z'  # 'Z' indicates UTC time

        # Create the task
        result = self.service.tasks().insert(tasklist=self.tasklist_id, body=task).execute()
        return result