# Cricket Auction Platform - Architecture Overview

## System Architecture

The Cricket Auction Platform is built with a clear separation between frontend and backend, communicating via REST API and WebSockets for real-time updates.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Nginx (Reverse Proxy)                   │
│                  Static Files + API Routing                 │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼────┐    ┌─────▼─────┐   ┌─────▼──────┐
   │ Angular │    │  FastAPI  │   │ WebSocket  │
   │ Frontend │    │  Backend  │   │ Server     │
   │ :4200   │    │  :8000    │   │ :8000      │
   └─────────┘    └─────┬─────┘   └────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼──────────┐ ┌──▼──┐       ┌────▼──────┐
   │ PostgreSQL DB │ │File │       │   Cache   │
   │ (Main DB)     │ │System       │  (Redis)  │
   │               │ │ uploads/    │  Optional │
   └───────────────┘ └─────┘       └───────────┘
```

## Technology Stack

### Backend
- **Framework:** FastAPI (async Python web framework)
- **ORM:** SQLAlchemy 2.0+ with async support
- **Database:** PostgreSQL 12+
- **Authentication:** PyJWT + OAuth2
- **Validation:** Pydantic V2
- **Image Processing:** Pillow (PIL)
- **Real-time:** WebSocket via FastAPI

### Frontend
- **Framework:** Angular 17+ (Standalone Components)
- **Language:** TypeScript 5+
- **Styling:** Tailwind CSS + Custom SCSS
- **UI Library:** PrimeNG 17+
- **State:** Angular Signals + RxJS
- **Real-time:** RxJS WebSocket Subject

### Infrastructure
- **Web Server:** Nginx (reverse proxy)
- **Process Manager:** PM2 (Python backend)
- **OS Support:** Linux, Windows, macOS
- **Environment:** .env configuration files

## Core Modules

### 1. Authentication & Authorization (Core Layer)
- JWT-based token management (access + refresh)
- Role-Based Access Control (RBAC) with 4 roles:
  - **Super Admin:** Full platform control
  - **Auction Manager:** Manage tournaments and auctions
  - **Franchise Owner:** Team management and bidding
  - **Viewer:** Read-only access
- Email verification for signups
- Secure password hashing (bcrypt)

### 2. Tournament Management
- Create/Edit/List tournaments with configurable rules
- Budget constraints and player limits
- Tournament status tracking (Planning, Active, Completed)
- Soft-delete support for audit trails

### 3. Team Management
- Team creation with owner assignment
- Logo upload (local storage with security)
- Budget allocation and tracking
- Team composition (players)

### 4. Player Management
- Player profiles with statistics
- Role categorization (Batsman, Bowler, All-rounder, Wicket-keeper)
- Base price setting
- Photo/video storage (local)
- Player availability management

### 5. Live Auction Engine (Core Feature)
- **Real-time Bidding:** WebSocket-driven updates
- **Auction Timer:** Server-side countdown (30s base, +10s per bid)
- **Bid Logic:**
  - Minimum bid increment enforcement
  - Auto-sold when timer expires
  - Bid validation against budget
- **Controls:**
  - Pause/Resume auction
  - Skip current player
  - Undo last bid
  - Mark as Sold/Unsold/Passed
- **Live Dashboard:**
  - Real-time leaderboard (teams ranked by purse spent)
  - Current purse display
  - Sold players list
  - Unsold players tracking

### 6. Bid History & Audit Trail
- Complete bid history with timestamps
- Soft-delete implementation (logical deletion)
- Restore capability for admins
- Historical data preservation for reporting

### 7. Reporting & Analytics
- Export to CSV/Excel/PDF (server-side generation)
- Dashboard metrics:
  - Total revenue/budget utilization
  - Player distribution by role
  - Team spending patterns
  - Franchise performance metrics
- Time-series analysis for bid trends

### 8. File Storage (Local Only)
- Structured upload directories:
  - `uploads/players/` - Player photos/videos
  - `uploads/teams/` - Team logos
  - `uploads/documents/` - Reports, exports
- Security measures:
  - File type validation
  - Size limits (configurable)
  - Unique filename generation
  - Directory traversal prevention
- Secure file serving via API endpoints or Nginx

## Database Design

### Soft Delete Strategy

All major entities implement soft deletes:

```sql
-- Every table has:
COLUMN is_deleted BOOLEAN DEFAULT FALSE
COLUMN deleted_at TIMESTAMP NULL
```

**Tables with Soft Delete:**
- `users`
- `tournaments`
- `teams`
- `players`
- `auctions`
- `bids`
- `bid_history`

**ORM Level:** SQLAlchemy implements a mixin that automatically filters `is_deleted=False` on queries.

**API Level:** "Delete" endpoints perform UPDATE operations, not physical DELETEs.

**Admin Panel:** Trash/Recover interface for deleted items.

## API Design Principles

1. **RESTful:** Standard HTTP methods (GET, POST, PUT, DELETE)
2. **Async:** All endpoints are async for high concurrency
3. **Pagination:** Implement offset/limit for large datasets
4. **Filtering:** Support query parameters for filtering
5. **Error Handling:** Consistent error response format with codes
6. **Validation:** Pydantic schemas for request/response validation
7. **Rate Limiting:** Protect endpoints from abuse

## WebSocket Architecture

### Real-time Auction Updates

**Endpoint:** `ws://localhost:8000/ws/auction/{auction_id}`

**Message Flow:**
1. Client connects to auction WebSocket
2. Server broadcasts:
   - Timer updates
   - New bids
   - Player status changes
   - Auction control events
3. Client updates UI in real-time

**Message Format:**
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

## Security Architecture

1. **Authentication:** JWT with 30-min access + 7-day refresh tokens
2. **Authorization:** Role-based guards on API endpoints
3. **Input Validation:** Pydantic V2 schemas
4. **SQL Injection Prevention:** SQLAlchemy ORM (no raw SQL)
5. **CORS:** Configured for frontend origin
6. **Rate Limiting:** Token bucket algorithm
7. **Password Security:** bcrypt hashing
8. **File Security:** Type/size validation, secure storage
9. **HTTPS Ready:** Nginx SSL/TLS support

## Deployment Architecture (Local)

### Service Layout

```
Linux/Windows/macOS Machine
├── PostgreSQL Server (Port 5432)
├── FastAPI Backend (Port 8000)
│   └── Managed by PM2
├── Angular Frontend Build (Nginx serving)
└── Nginx Reverse Proxy (Port 80/443)
    ├── Routes /api → FastAPI
    ├── Routes /ws → FastAPI WebSocket
    └── Routes / → Angular static files
```

### Environment Variables

All configuration via `.env` file (no hardcoded secrets):
- Database connection
- JWT secrets
- Upload paths
- CORS origins
- Email configuration

## Performance Considerations

1. **Database Indexes:** On foreign keys and frequently filtered columns
2. **Async Queries:** Non-blocking database operations
3. **Connection Pooling:** SQLAlchemy connection pool configuration
4. **Caching:** Redis for auction state (optional)
5. **WebSocket Optimization:** Efficient message broadcasting
6. **Frontend Bundling:** Angular CLI production builds

## Scalability Notes

- **Stateless Backend:** Multiple FastAPI instances can run behind load balancer
- **Database:** PostgreSQL handles concurrent users well
- **WebSocket:** Consider Redis pub/sub for multi-instance deployments
- **File Storage:** Local storage suitable for single-server deployments

## Monitoring & Logging

- **Backend Logs:** Structured logging to files and console
- **Database Logs:** PostgreSQL slow query log
- **Frontend Errors:** Console logging and error tracking
- **PM2 Monitoring:** Process health and resource usage
