"""Auction Model"""
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum

from app.models.base import Base

# Association table for many-to-many relationship between Auction and Team
auction_teams = Table(
    "auction_teams",
    Base.metadata,
    Column("auction_id", Integer, ForeignKey("auctions.id", ondelete="CASCADE")),
    Column("team_id", Integer, ForeignKey("teams.id", ondelete="CASCADE")),
)


class AuctionStatusEnum(str, enum.Enum):
    """Auction status."""
    SCHEDULED = "scheduled"
    LIVE = "live"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Auction(Base):
    """Auction model."""
    __tablename__ = "auctions"

    name = Column(String(255), nullable=False, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id", ondelete="CASCADE"), nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), default=AuctionStatusEnum.SCHEDULED, nullable=False)
    current_player_id = Column(Integer, ForeignKey("players.id"), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    is_live = Column(Boolean, default=False, nullable=False)

    # Relationships
    tournament = relationship("Tournament", back_populates="auctions")
    manager = relationship("User", back_populates="auctions_managed", foreign_keys=[manager_id])
    teams = relationship("Team", secondary=auction_teams, back_populates="auction_teams")
    bids = relationship("Bid", back_populates="auction", cascade="all, delete-orphan")
    bid_history = relationship("BidHistory", back_populates="auction", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Auction {self.name}>"
