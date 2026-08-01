# AI-Powered Business Analytics Assistant

This is the foundational architecture for an enterprise-grade AI-powered Business Analytics Assistant. It is designed to be highly maintainable, scalable, modular, and ready for production deployment.

## Architecture

The project follows a strict Layered Architecture on the backend and a modular structure on the frontend.

- **Backend**: Python 3.12, FastAPI, PostgreSQL, SQLAlchemy, Pydantic, Alembic
- **Frontend**: React 19, TypeScript, Vite, TailwindCSS
- **Infrastructure**: Docker, Docker Compose, Nginx

## Quick Start (Docker)

1. Copy the environment variables:
   ```bash
   cp .env.example .env
   ```
2. Start the services:
   ```bash
   docker compose up -d --build
   ```
3. Access the application:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

## Development Setup

Please refer to the `README.md` files located in the `backend/` and `frontend/` directories for detailed local setup instructions.
