"""Reporting and analytics routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/auction/{auction_id}/summary")
async def get_auction_summary(
    auction_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get auction summary report."""
    # TODO: Implement report service
    pass
