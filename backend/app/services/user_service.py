"""User business logic service."""
import logging
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.core.security import hash_password
from app.schemas.user import UserCreate, UserUpdate

logger = logging.getLogger(__name__)


class UserService:
    """User service for database operations."""

    @staticmethod
    async def get_user(db: AsyncSession, user_id: int) -> User | None:
        """Get user by ID."""
        stmt = select(User).where(
            (User.id == user_id) & (User.is_deleted == False)
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
        """Get user by email."""
        stmt = select(User).where(
            (User.email == email) & (User.is_deleted == False)
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
        """Get user by username."""
        stmt = select(User).where(
            (User.username == username) & (User.is_deleted == False)
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        """Create a new user."""
        user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            password_hash=hash_password(user_data.password),
            role=user_data.role,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"User created: {user.username}")
        return user

    @staticmethod
    async def update_user(db: AsyncSession, user: User, update_data: UserUpdate) -> User:
        """Update user information."""
        update_fields = update_data.dict(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(user, field, value)
        user.updated_at = datetime.now(timezone.utc)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"User updated: {user.username}")
        return user

    @staticmethod
    async def soft_delete_user(db: AsyncSession, user: User) -> None:
        """Soft delete a user."""
        user.soft_delete()
        db.add(user)
        await db.commit()
        logger.info(f"User soft deleted: {user.username}")

    @staticmethod
    async def list_users(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> list[User]:
        """List all users."""
        stmt = select(User).where(User.is_deleted == False).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def update_last_login(db: AsyncSession, user: User) -> None:
        """Update user's last login timestamp."""
        user.last_login_at = datetime.now(timezone.utc)
        db.add(user)
        await db.commit()
