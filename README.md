# Cricket Auction Platform

A production-ready Cricket Auction Platform (similar to IPL Auction software) built with FastAPI (Python backend) and Angular 17+ (frontend).

## Quick Start

1. Clone the repository
2. Follow the [Local Setup Guide](./docs/SETUP.md)
3. Start the application using the provided scripts

## Tech Stack

- **Backend:** Python 3.10+, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend:** Angular 17+, TypeScript, Tailwind CSS, PrimeNG
- **Real-time:** WebSockets via FastAPI
- **Authentication:** JWT + OAuth2
- **File Storage:** Local uploads directory

## Features

- Role-Based Access Control (RBAC)
- Tournament & Team Management
- Live Auction Engine with WebSocket real-time bidding
- Bid history and soft delete preservation
- CSV/Excel/PDF reporting
- Secure local file uploads

## Documentation

- [Architecture Overview](./docs/ARCHITECTURE.md)
- [API Documentation](./backend/README.md)
- [Frontend Guide](./frontend/README.md)
- [Database Schema](./docs/DATABASE.md)
- [Local Setup Instructions](./docs/SETUP.md)

## Project Structure

```
cricket_auction/
├── backend/              # FastAPI backend
├── frontend/             # Angular frontend
├── nginx/                # Nginx reverse proxy config
├── scripts/              # Setup and startup scripts
├── docs/                 # Documentation
└── .env.example          # Environment variables template
```
