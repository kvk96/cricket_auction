"""Team management routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/")
async def list_teams(
    tournament_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List teams in a tournament."""
    # TODO: Implement list service
    pass


@router.post("/")
async def create_team(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new team."""
    # TODO: Implement create service
    pass
