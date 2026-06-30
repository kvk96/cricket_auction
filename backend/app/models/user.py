"""User Model"""
from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum

from app.models.base import Base


class RoleEnum(str, enum.Enum):
    """User roles for RBAC."""
    SUPER_ADMIN = "super_admin"
    AUCTION_MANAGER = "auction_manager"
    FRANCHISE_OWNER = "franchise_owner"
    VIEWER = "viewer"


class Role(Base):
    """Role model."""
    __tablename__ = "roles"

    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255))
    permissions = relationship("Permission", back_populates="role", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Role {self.name}>"


class User(Base):
    """User model with soft delete support."""
    __tablename__ = "users"

    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.VIEWER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    profile_photo_url = Column(String(500), nullable=True)

    # Relationships
    teams = relationship("Team", back_populates="owner", foreign_keys="Team.owner_id")
    auctions_managed = relationship("Auction", back_populates="manager", foreign_keys="Auction.manager_id")
    bids = relationship("Bid", back_populates="bidder", foreign_keys="Bid.bidder_id")

    def __repr__(self):
        return f"<User {self.username}>"

    @property
    def is_admin(self) -> bool:
        """Check if user is admin."""
        return self.role in [RoleEnum.SUPER_ADMIN, RoleEnum.AUCTION_MANAGER]
