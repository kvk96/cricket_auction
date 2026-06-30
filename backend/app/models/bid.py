"""Bid and Bid History Models"""
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.models.base import Base


class Bid(Base):
    """Current bid model."""
    __tablename__ = "bids"

    auction_id = Column(Integer, ForeignKey("auctions.id", ondelete="CASCADE"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    bidder_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    is_winning_bid = Column(Boolean, default=True, nullable=False)

    # Relationships
    auction = relationship("Auction", back_populates="bids")
    player = relationship("Player", back_populates="bids")
    team = relationship("Team", back_populates="bids")
    bidder = relationship("User", back_populates="bids", foreign_keys=[bidder_id])

    def __repr__(self):
        return f"<Bid {self.amount} for {self.player_id}>"


class BidHistory(Base):
    """Bid history for audit trail."""
    __tablename__ = "bid_history"

    auction_id = Column(Integer, ForeignKey("auctions.id", ondelete="CASCADE"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    bidder_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    bid_number = Column(Integer, nullable=False)  # Sequential bid number
    status = Column(String(50), nullable=False)  # 'active', 'outbid', 'won', 'cancelled'
    notes = Column(String(500), nullable=True)

    # Relationships
    auction = relationship("Auction", back_populates="bid_history")
    player = relationship("Player", back_populates="bid_history")

    def __repr__(self):
        return f"<BidHistory #{self.bid_number} - {self.amount}>"
