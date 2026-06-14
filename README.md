# MultiMeet

Real-time video conferencing platform inspired by Google Meet. Built with FastAPI (Clean Architecture), PostgreSQL, and LiveKit (WebRTC).

## Architecture

```text
root/
├── docker-compose.yml     ← orchestrates all services
├── livekit.yaml           ← LiveKit server configuration
├── AGENTS.md              ← project conventions & rules
├── meeting/               ← FastAPI backend (Clean Architecture)
│   ├── Dockerfile         ← multi-stage, non-root container
│   ├── main.py
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── presentation/
└── README.md
```

## Quick Start

### Prerequisites

- Docker & Docker Compose v2
- Git

### 1. Clone & initialize

```bash
git clone <repo-url> multimeet
cd multimeet
```

### 2. Configure environment

```bash
cp meeting/.env.example meeting/.env
# Edit meeting/.env with your secrets if needed
```

### 3. Build & start the full stack

```bash
docker-compose up -d --build
```

This starts three services:

| Service  | Port(s)           | Description                      |
| -------- | ----------------- | -------------------------------- |
| `api`    | `8000`            | FastAPI backend                  |
| `db`     | `5432`            | PostgreSQL database              |
| `livekit`| `7880`, `7882`    | WebRTC media server (sidecar)    |

### 4. Run database migrations

```bash
docker-compose exec api alembic upgrade head
```

### 5. Verify

Open [http://localhost:8000/docs](http://localhost:8000/docs) for the Swagger UI.

## Commands Reference

| Action                      | Command                                                       |
| --------------------------- | ------------------------------------------------------------- |
| Build & start               | `docker-compose up -d --build`                                |
| Stop all services           | `docker-compose down`                                         |
| View API logs               | `docker-compose logs -f api`                                  |
| View LiveKit logs           | `docker-compose logs -f livekit`                              |
| Shell into API container    | `docker-compose exec api /bin/sh`                             |
| Apply migrations            | `docker-compose exec api alembic upgrade head`                |
| Create a migration          | `docker-compose exec api alembic revision --autogenerate -m "desc"` |
| Rollback one migration      | `docker-compose exec api alembic downgrade -1`                |
| Rebuild single service      | `docker-compose up -d --build api`                            |

## LiveKit (WebRTC)

LiveKit runs as a Docker sidecar alongside the API and database. The FastAPI backend generates LiveKit JWT tokens for authenticated users — media never flows through the Python backend.

- **Signal port**: `7880` (WebSocket, client ↔ LiveKit)
- **Media port**: `7882` (UDP/TCP relay)

Configuration is in `livekit.yaml` at the repository root. The `devkey`/`devsecret` pair there must match `LIVEKIT_API_KEY`/`LIVEKIT_API_SECRET` in the API container's environment.

## Development (without Docker)

```bash
cd meeting
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Requires a local PostgreSQL instance. Set `DATABASE_URL` in `meeting/.env`.

## Project Structure

```text
meeting/
├── Dockerfile                # Multi-stage, non-root user
├── main.py                   # FastAPI composition root
├── requirements.txt
├── alembic.ini / alembic/    # Database migrations
├── domain/                   # Entities, repository interfaces, exceptions
│   ├── entity/
│   └── repository_interface/
├── application/usecases/     # Business logic (RBAC-enforced)
├── infrastructure/           # ORM models, repositories, security, DI providers
│   ├── orm/
│   ├── repository/
│   └── provider/
└── presentation/             # Routers, DTOs, presenters, auth stubs
    ├── router/
    ├── dto/
    ├── presenter/
    └── dependencies/
```

## License

MIT
