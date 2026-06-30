"""Tournament management routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.schemas.tournament import TournamentCreate, TournamentResponse, TournamentUpdate
from app.models.user import User, RoleEnum

router = APIRouter()


@router.post("/", response_model=TournamentResponse, status_code=status.HTTP_201_CREATED)
async def create_tournament(
    tournament_data: TournamentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new tournament (manager+ only)."""
    if current_user.role not in [RoleEnum.SUPER_ADMIN, RoleEnum.AUCTION_MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tournaments",
        )
    # TODO: Implement tournament creation service
    pass


@router.get("/", response_model=List[TournamentResponse])
async def list_tournaments(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List all tournaments."""
    # TODO: Implement list service
    pass


@router.get("/{tournament_id}", response_model=TournamentResponse)
async def get_tournament(
    tournament_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get tournament by ID."""
    # TODO: Implement get service
    pass


@router.put("/{tournament_id}", response_model=TournamentResponse)
async def update_tournament(
    tournament_id: int,
    update_data: TournamentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update tournament (manager+ only)."""
    if current_user.role not in [RoleEnum.SUPER_ADMIN, RoleEnum.AUCTION_MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )
    # TODO: Implement update service
    pass
