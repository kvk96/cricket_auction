"""Tournament Model"""
from sqlalchemy import Column, String, Integer, Float, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum

from app.models.base import Base


class TournamentStatusEnum(str, enum.Enum):
    """Tournament status."""
    PLANNING = "planning"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Tournament(Base):
    """Tournament model."""
    __tablename__ = "tournaments"

    name = Column(String(255), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    status = Column(Enum(TournamentStatusEnum), default=TournamentStatusEnum.PLANNING, nullable=False)
    total_budget = Column(Float, nullable=False)  # In currency units
    min_players_per_team = Column(Integer, default=15, nullable=False)
    max_players_per_team = Column(Integer, default=25, nullable=False)
    total_players = Column(Integer, nullable=False)  # Total players in tournament
    logo_url = Column(String(500), nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    teams = relationship("Team", back_populates="tournament", cascade="all, delete-orphan")
    players = relationship("Player", back_populates="tournament", cascade="all, delete-orphan")
    auctions = relationship("Auction", back_populates="tournament", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Tournament {self.name}>"
