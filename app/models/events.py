from datetime import datetime

from pydantic import BaseModel


class Event(BaseModel):
    id: str
    name: str
    date: datetime


class EventAdd(BaseModel):
    name: str
    date: datetime
