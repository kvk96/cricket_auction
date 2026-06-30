"""Cricket Auction Platform - FastAPI Entry Point"""
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import engine, init_db
from app.api import auth, users, tournaments, teams, players, auctions, bids, reports
from app.websockets import auction_ws

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Manage application lifespan - startup and shutdown events."""
    # Startup
    logger.info("Starting Cricket Auction Platform...")
    await init_db()
    logger.info("Database initialized")
    yield
    # Shutdown
    logger.info("Shutting down Cricket Auction Platform...")


# Initialize FastAPI app
app = FastAPI(
    title="Cricket Auction Platform API",
    description="Production-ready cricket auction management system",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)


# Global exception handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "1.0.0"}


# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(tournaments.router, prefix="/api/v1/tournaments", tags=["Tournaments"])
app.include_router(teams.router, prefix="/api/v1/teams", tags=["Teams"])
app.include_router(players.router, prefix="/api/v1/players", tags=["Players"])
app.include_router(auctions.router, prefix="/api/v1/auctions", tags=["Auctions"])
app.include_router(bids.router, prefix="/api/v1/bids", tags=["Bids"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(auction_ws.router, tags=["WebSocket"])

# Serve static files (uploads)
import os
if not os.path.exists(settings.UPLOAD_DIRECTORY):
    os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory=settings.UPLOAD_DIRECTORY),
    name="uploads",
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
