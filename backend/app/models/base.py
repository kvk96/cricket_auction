"""Base model with common fields."""
from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, Column
from sqlalchemy.orm import declarative_base, declared_attr
from app.core.soft_delete import SoftDeleteMixin


class BaseModel(SoftDeleteMixin):
    """Base model with common fields and soft delete support."""

    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True, index=True)

    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


Base = declarative_base(cls=BaseModel)
