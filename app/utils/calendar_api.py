import os
from datetime import datetime, timedelta, timezone
from typing import Union, List, Any

import googleapiclient
from dotenv import load_dotenv
from fastapi import HTTPException
from google.oauth2 import service_account

from app.models import Event

load_dotenv()

from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

CALENDAR_ID = os.getenv("CALENDAR_ID")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")


class CalendarAPI:
    """Google Calendar api management class"""

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(f'{SERVICE_ACCOUNT_FILE}.json',
                                                                            scopes=SCOPES)
        self.service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

    def get_events(self, date: Union[None, str] = None) -> List[Event]:
        """Get week events for the specified date

        Args:
            date (str): Date of the week you are looking for in the format '%Y-%m-%d'.

        Returns:
            List[Event]: All Events of the week.
        """

        datetime_object = None

        try:
            datetime_object = datetime.strptime(date, '%Y-%m-%d')
        except:
            pass

        now = datetime_object if datetime_object else datetime.utcnow()

        start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0)
        end = (start + timedelta(days=7)).replace(hour=0, minute=0, second=0)

        events = self.service.events().list(calendarId=CALENDAR_ID,
                                            timeMin=self._format_date(start),
                                            timeMax=self._format_date(end)).execute()

        result: List[Event] = []

        print(events['items'])

        for item in events['items']:
            result.append(Event(
                id=item['id'],
                name=item['summary'],
                date=item['start']['dateTime']
            ))

        return result

    def add_event(self, event: Event) -> Event:
        """Add an event to the calendar

        Args:
            event (Event): The calendar event object.

        Returns:
            Event: newly added calendar event object.
        """

        start = event.date.astimezone(tz=timezone.utc).replace(tzinfo=None)
        end = start + timedelta(hours=1)

        is_busy = bool(self.service.events().list(calendarId=CALENDAR_ID,
                                                  timeMin=self._format_date(start),
                                                  timeMax=self._format_date(end)).execute()['items'])

        if is_busy:
            raise HTTPException(status_code=400, detail="This slot is busy. Try another.")

        event = self.service.events().insert(calendarId=CALENDAR_ID,
                                             body=self._format_event(event)).execute()

        return Event(
            id=event['id'],
            name=event['summary'],
            date=event['start']['dateTime']
        )

    def _format_date(self, date: datetime) -> str:
        """Format a date to the Google Calendar datetime format"""

        return date.isoformat() + 'Z'

    def _format_event(self, event: Event) -> Any:
        """Format an event to the Google Calendar event format"""

        return {
            "summary": event.name,
            "start": {
                "dateTime": event.date.isoformat(),
                "timeZone": "Europe/Moscow"
            },
            "end": {
                "dateTime": (event.date + timedelta(hours=1)).isoformat(),
                "timeZone": "Europe/Moscow"
            }
        }


calendar = CalendarAPI()
