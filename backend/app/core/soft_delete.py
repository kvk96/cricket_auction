"""Soft delete mixin for SQLAlchemy models."""
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, desc
from sqlalchemy.orm import declared_attr
from sqlalchemy.ext.declarative import declarative_base


class SoftDeleteMixin:
    """Mixin to add soft delete functionality to models."""

    @declared_attr
    def is_deleted(cls):
        return Boolean(default=False, nullable=False)

    @declared_attr
    def deleted_at(cls):
        return DateTime(timezone=True, nullable=True)

    def soft_delete(self):
        """Mark record as deleted without physical deletion."""
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self):
        """Restore a soft-deleted record."""
        self.is_deleted = False
        self.deleted_at = None
