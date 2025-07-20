import os
import datetime
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from langchain.tools import BaseTool
from typing import Optional, Type, Union
from pydantic import BaseModel, Field
from dateutil.parser import parse
from zoneinfo import ZoneInfo

# --- Google Calendar API Authentication (MODIFIED FOR MULTI-USER) ---
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service(username: str):
    """
    Authenticates with Google Calendar API for a specific user.
    Uses a unique token file for each user (e.g., 'mdsalique_token.pickle').
    """
    creds = None
    token_file = f'{username}_token.pickle'

    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

# --- LangChain Tools (MODIFIED TO ACCEPT USERNAME) ---
class CreateEventInput(BaseModel):
    summary: Union[str, dict] = Field(description="The title or summary of the event.")
    start_time: str = Field(description="The start time of the event in a standard date-time format.")
    end_time: str = Field(description="The end time of the event in a standard date-time format.")
    attendees: Optional[list[str]] = Field(default=None, description="A list of email addresses of the attendees.")

class CreateCalendarEventTool(BaseTool):
    name: str = "create_calendar_event"
    description: str = "Use this tool to create a new event on the Google Calendar."
    args_schema: Type[BaseModel] = CreateEventInput
    username: str

    def _run(self, summary: Union[str, dict], start_time: str, end_time: str, attendees: Optional[list[str]] = None):
        try:
            if isinstance(summary, dict):
                event_summary = summary.get('summary') or summary.get('title') or 'Untitled Event'
            else:
                event_summary = summary

            service = get_calendar_service(self.username)
            local_tz = ZoneInfo("Asia/Kolkata")
            
            naive_start_dt = parse(start_time, ignoretz=True)
            naive_end_dt = parse(end_time, ignoretz=True)

            aware_start_dt = naive_start_dt.replace(tzinfo=local_tz)
            aware_end_dt = naive_end_dt.replace(tzinfo=local_tz)

            event = {
                'summary': event_summary,
                'start': {'dateTime': aware_start_dt.isoformat(), 'timeZone': str(local_tz)},
                'end': {'dateTime': aware_end_dt.isoformat(), 'timeZone': str(local_tz)},
            }
            if attendees:
                event['attendees'] = [{'email': email} for email in attendees]

            created_event = service.events().insert(calendarId='primary', body=event).execute()
            return f"Event created successfully! View it here: {created_event.get('htmlLink')}"
        except Exception as e:
            return f"An error occurred while creating the event: {e}"

class ListEventsInput(BaseModel):
    start_time: str = Field(description="The start of the time window to check for events.")
    end_time: str = Field(description="The end of the time window to check for events.")

class ListCalendarEventsTool(BaseTool):
    name: str = "list_calendar_events"
    description: str = "Use this tool to list events from the Google Calendar."
    args_schema: Type[BaseModel] = ListEventsInput
    username: str

    def _run(self, start_time: str, end_time: str):
        try:
            service = get_calendar_service(self.username)
            local_tz = ZoneInfo("Asia/Kolkata")
            
            naive_start_dt = parse(start_time, ignoretz=True)
            naive_end_dt = parse(end_time, ignoretz=True)

            aware_start_dt = naive_start_dt.replace(tzinfo=local_tz)
            aware_end_dt = naive_end_dt.replace(tzinfo=local_tz)
            
            events_result = service.events().list(
                calendarId='primary', 
                timeMin=aware_start_dt.isoformat(),
                timeMax=aware_end_dt.isoformat(),
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            if not events: return "No upcoming events found."

            event_list = [f"- {event['summary']} (at {parse(event['start'].get('dateTime', event['start'].get('date'))).strftime('%I:%M %p on %A, %B %d')})" for event in events]
            return "Here are the events:\n" + "\n".join(event_list)
        except Exception as e:
            return f"An error occurred while listing events: {e}"

class SummarizeMeetingTool(BaseTool):
    name: str = "summarize_last_meeting"
    description: str = "Use this tool to get a summary of the most recent meeting."
    args_schema: Type[BaseModel] = ListEventsInput
    username: str

    def _run(self, *args, **kwargs):
        return "Placeholder Summary: The last meeting discussed Q3 project milestones."