# Trendly Agentic Support Assistant

This repository contains the codebase for Trendly's Agentic Customer Support system. It combines a Next.js frontend with a FastAPI backend, utilizing OpenRouter LLM capabilities strictly for reasoning and orchestration over deterministic domain tools and services.

## Architecture

The system uses a logical microservices pattern deployed within a single FastAPI app:
- **Frontend**: Next.js (React, Tailwind)
- **API**: FastAPI (Python)
- **Conversation Service**: Manages multi-turn state and session context.
- **Orchestrator**: Interacts with the LLM and orchestrates deterministic tool calls.
- **Services (Order, Policy, Returns, Exchanges, Escalations)**: Deterministic execution of business rules.

## Setup
### Backend
1. Python 3.11+ is required.
2. Setup a virtual environment: `python -m venv venv`
3. Activate the virtual environment.
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and set `OPENROUTER_API_KEY`.
6. Start the backend: `python -m apps.api.main`

### Frontend
1. Node.js is required.
2. Navigate to `frontend/`
3. Run `npm install`
4. Start the development server: `npm run dev`

## Usage
Open `http://localhost:3000` to interact with the support assistant.
The backend API is running on `http://localhost:8000`.
