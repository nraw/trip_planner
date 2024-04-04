from datetime import datetime

from pydantic import BaseModel, Field


class Schedule(BaseModel):
    num_days: int
    start_date: datetime
    # TODO: parse datetime nicely please?


class TripRequest(BaseModel):
    destination: str
    start: str
    end: str
    details: list[str]


class BroadRecommendations(BaseModel):
    sights: list[str]
    trips: list[str]
    activities: list[str]
    events: list[str]


class DailyAgenda(BaseModel):
    day: int
    date: str
    sights: list[str]
    activities: list[str]


class TripAgenda(BaseModel):
    agenda: list[DailyAgenda]
