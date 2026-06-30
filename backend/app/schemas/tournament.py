"""Tournament schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.tournament import TournamentStatusEnum


class TournamentBase(BaseModel):
    """Base tournament schema."""
    name: str
    description: Optional[str] = None
    total_budget: float
    min_players_per_team: int = 15
    max_players_per_team: int = 25
    total_players: int


class TournamentCreate(TournamentBase):
    """Tournament creation schema."""
    pass


class TournamentUpdate(BaseModel):
    """Tournament update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TournamentStatusEnum] = None
    total_budget: Optional[float] = None


class TournamentResponse(TournamentBase):
    """Tournament response schema."""
    id: int
    status: TournamentStatusEnum
    logo_url: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
