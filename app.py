from dotenv import load_dotenv
import os
from authentication import Authentication

# Load environment variables
load_dotenv()
calendar_id = os.getenv('CALENDAR_ID')

# Establish Authentication
auth = Authentication()
service = auth.build_service()