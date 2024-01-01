class Task:
    def __init__(self, service):
        self.service = service
        self.tasklist_id = None

    def get_all_tasklists(self):
        """Get and return all task lists"""
        # Get the list of task lists
        tasklists = self.service.tasklists().list().execute()

        # Store each task list in a dictionary
        tasklist_dict = {}
        for tasklist in tasklists['items']:
            tasklist_dict[tasklist['title']] = tasklist['id']

        return tasklist_dict

    def select_tasklist(self):
        """Ask the user to select a task list and return its ID"""
        # Get all tasklists
        all_tasklists = self.get_all_tasklists()

        # Print all tasklists with a number
        for i, tasklist_name in enumerate(all_tasklists, start=1):
            print(f"{i}. {tasklist_name}")

        while True:
            try:
                # Ask the user to select a tasklist by number
                selected_index = int(input("Please select a tasklist by number: ")) - 1

                # Check if the selected index is within the range of available tasklists
                if selected_index < 0 or selected_index >= len(all_tasklists):
                    print("Invalid selection. Please select a number within the range of available tasklists.")
                    continue

                # Get the selected tasklist name
                selected_tasklist_name = list(all_tasklists.keys())[selected_index]

                # Set the tasklist_id attribute
                self.tasklist_id = all_tasklists.get(selected_tasklist_name, '@default')

                # Print the selected tasklist
                print(f"You have selected: {selected_tasklist_name}")

                # Return the selected tasklist ID
                return self.tasklist_id
            except ValueError:
                print("Invalid input. Please enter a number.")

    def create_task(self, title, notes, due_date=None):
        """Create a new task in the specified task list"""
        try:
            # Ensure that notes is a string
            if isinstance(notes, tuple):
                notes = notes[0] if notes else ''

            # Define the task
            task = {
                'title': title,
                'notes': notes,
            }
            if due_date:
                task['due'] = due_date.isoformat()+'Z'  # 'Z' indicates UTC time

            # Create the task
            result = self.service.tasks().insert(tasklist=self.tasklist_id, body=task).execute()

            # Print the title and notes of the created task
            notes = result.get('notes')
            if notes is None:
                notes = "No description"
            print(f"Created \"{result['title']}\" {notes}.")

            return result

        except Exception as e:
            print(f"An error occurred: {e}")