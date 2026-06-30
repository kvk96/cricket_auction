# Cricket Auction Platform - Backend

## Overview

FastAPI-based backend for the Cricket Auction Platform with real-time WebSocket support, JWT authentication, and SQLAlchemy ORM.

## Tech Stack

- **Framework:** FastAPI 0.104+
- **Server:** Uvicorn
- **Database:** PostgreSQL with SQLAlchemy 2.0
- **Authentication:** JWT + OAuth2
- **Real-time:** WebSockets
- **Validation:** Pydantic V2
- **Image Processing:** Pillow

## Project Structure

```
backend/
├── app/
│   ├── api/                 # API route handlers
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── users.py        # User management
│   │   ├── tournaments.py  # Tournament management
│   │   ├── teams.py        # Team management
│   │   ├── players.py      # Player management
│   │   ├── auctions.py     # Auction management
│   │   ├── bids.py         # Bid management
│   │   └── reports.py      # Reporting & analytics
│   ├── core/
│   │   ├── config.py       # Application configuration
│   │   ├── database.py     # Database setup
│   │   ├── security.py     # JWT & password utilities
│   │   └── soft_delete.py  # Soft delete mixin
│   ├── models/
│   │   ├── base.py         # Base model class
│   │   ├── user.py         # User & Role models
│   │   ├── tournament.py   # Tournament model
│   │   ├── team.py         # Team model
│   │   ├── player.py       # Player model
│   │   ├── auction.py      # Auction model
│   │   └── bid.py          # Bid models
│   ├── schemas/
│   │   ├── user.py         # User Pydantic schemas
│   │   └── tournament.py   # Tournament Pydantic schemas
│   ├── services/
│   │   └── user_service.py # User business logic
│   └── websockets/
│       └── auction_ws.py   # WebSocket handlers
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL 12+
- pip or poetry

### Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize database:**
   ```bash
   # Database should be created in PostgreSQL first
   # Tables will be created automatically on first run
   ```

## Running the Application

### Development Mode

```bash
python main.py
```

Server will start on `http://127.0.0.1:8000`

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Authentication

All protected endpoints require a JWT token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

### Login Flow

1. **POST** `/api/v1/auth/login` - Get access and refresh tokens
2. **POST** `/api/v1/auth/refresh` - Refresh expired access token
3. **GET** `/api/v1/auth/me` - Get current user info

## Database

### Migrations

Use Alembic for database migrations:

```bash
# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head
```

## Real-time Features

### WebSocket Connections

**Auction Updates:** `ws://localhost:8000/ws/auction/{auction_id}`

Message format:
```json
{
  "type": "bid",
  "data": {
    "bid_id": "123",
    "amount": 1500000,
    "team_id": "abc",
    "timestamp": "2026-06-30T12:00:00Z"
  }
}
```

## Configuration

All configuration is loaded from `.env` file:

- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT signing key (min 32 characters)
- `BACKEND_HOST` - Server host (default: 127.0.0.1)
- `BACKEND_PORT` - Server port (default: 8000)
- `DEBUG` - Debug mode (default: False)
- `CORS_ORIGINS` - Allowed CORS origins

## Testing

```bash
pytest
```

## Security Notes

1. **Never commit `.env` file** with sensitive data
2. **Change `SECRET_KEY`** in production
3. **Use HTTPS** in production
4. **Enable CORS** only for trusted origins
5. **Implement rate limiting** on public endpoints

## Troubleshooting

### Database Connection Error

Ensure PostgreSQL is running and connection string is correct in `.env`

### Port Already in Use

Change port in `.env` or kill existing process:
```bash
lsof -ti:8000 | xargs kill -9  # Linux/macOS
```

## Contributing

Follow these guidelines:

- Use async/await for all database operations
- Implement soft delete for all major entities
- Add unit tests for new services
- Follow PEP 8 style guide
- Document complex logic with docstrings
