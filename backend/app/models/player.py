"""Player Model"""
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.models.base import Base


class PlayerRoleEnum(str, enum.Enum):
    """Player cricket roles."""
    BATSMAN = "batsman"
    BOWLER = "bowler"
    ALL_ROUNDER = "all_rounder"
    WICKET_KEEPER = "wicket_keeper"


class Player(Base):
    """Player model."""
    __tablename__ = "players"

    name = Column(String(255), nullable=False, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id", ondelete="CASCADE"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="SET NULL"), nullable=True)
    role = Column(Enum(PlayerRoleEnum), nullable=False)
    base_price = Column(Float, nullable=False)  # Starting/base price
    country = Column(String(100), nullable=True)
    batting_style = Column(String(50), nullable=True)  # e.g., "Right-handed"
    bowling_style = Column(String(50), nullable=True)  # e.g., "Right-arm Fast"
    photo_url = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)
    jersey_number = Column(Integer, nullable=True)
    is_available = Column(Integer, default=1, nullable=False)  # 1: Available, 0: Sold, -1: Unsold/Passed
    notes = Column(String(1000), nullable=True)

    # Relationships
    tournament = relationship("Tournament", back_populates="players")
    team = relationship("Team", back_populates="players")
    bids = relationship("Bid", back_populates="player")
    bid_history = relationship("BidHistory", back_populates="player")

    def __repr__(self):
        return f"<Player {self.name}>"
