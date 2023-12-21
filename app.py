from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import pytz,dateutil.parser, os
from dateutil.parser import parse
import pickle
from dotenv import load_dotenv
from authentication import Authentication

## Load environment variables
load_dotenv()
calendar_id = os.getenv('CALENDAR_ID')

## Establish Authentication
auth = Authentication()
service = auth.build_service()

## Get the current time
now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print(f'Getting Tomorrow\'s events')
tomorrow = datetime.utcnow() + timedelta(days=1)
tomorrow = tomorrow.isoformat() + 'Z'


