"""Team Model"""
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.models.base import Base


class Team(Base):
    """Team model."""
    __tablename__ = "teams"

    name = Column(String(255), nullable=False, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id", ondelete="CASCADE"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    abbreviation = Column(String(10), nullable=False)
    logo_url = Column(String(500), nullable=True)
    budget_allocated = Column(Float, nullable=False)  # Total budget for this team
    budget_remaining = Column(Float, nullable=False)  # Remaining budget
    players_count = Column(Integer, default=0, nullable=False)
    city = Column(String(100), nullable=True)

    # Relationships
    tournament = relationship("Tournament", back_populates="teams")
    owner = relationship("User", back_populates="teams", foreign_keys=[owner_id])
    players = relationship("Player", back_populates="team")
    auction_teams = relationship("Auction", secondary="auction_teams", back_populates="teams")
    bids = relationship("Bid", back_populates="team")

    def __repr__(self):
        return f"<Team {self.name}>"

    @property
    def budget_used(self) -> float:
        """Calculate budget used."""
        return self.budget_allocated - self.budget_remaining
