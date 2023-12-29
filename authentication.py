from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth import exceptions
import os
import pickle

class Authentication:
    def purge_expired_token(self):
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'rb') as token:
                credentials = pickle.load(token)
            if credentials.expired:
                os.remove(self.credentials_file)
                
    def __init__(self, credentials_file='token.pickle', client_secret_file='client_secret.json'):
        self.credentials_file = credentials_file
        self.client_secret_file = client_secret_file
        self.credentials = self.load_credentials()


   ## TODO Refactor the build_service method into build_calendar_service - which will requoire a full refactor of the app.py file
    def build_service(self):
        return build('calendar', 'v3', credentials=self.credentials)
    
    def build_tasks_service(self):
        return build('tasks', 'v1', credentials=self.credentials)

    def load_credentials(self):
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'rb') as token:
                credentials = pickle.load(token)
        else:
            credentials = None

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                try:
                    credentials.refresh(Request())
                except exceptions.RefreshError:
                    os.remove(self.credentials_file)
                    return self.load_credentials()
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secret_file, ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/tasks'])
                credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.credentials_file, 'wb') as token:
                pickle.dump(credentials, token)

        return credentials