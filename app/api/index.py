from typing import Union, List

from fastapi import APIRouter, Body

from app.models import EventAdd, Event
from app.utils import calendar

router = APIRouter()


@router.get("/", response_model=List[Event], response_description="Get the schedule for this week")
async def get_schedule(dt: Union[str, None] = None):
    return calendar.get_events(date=dt)


@router.post("/", response_model=Event, response_description="Add an event to the schedule")
async def add_event(payload: EventAdd = Body()):
    return calendar.add_event(event=payload)
