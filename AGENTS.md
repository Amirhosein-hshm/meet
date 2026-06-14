AGENTS.md — MultiMeet Project

## Project Overview

Monorepo for a real-time video conferencing platform (inspired by Google Meet). The backend API lives under `meeting/` and is built with **Python 3.12+**, **FastAPI**, **SQLAlchemy 2.0**, **PostgreSQL**, **Pydantic v2**, **JWT**, **Alembic**. LiveKit server runs as a Docker sidecar for WebRTC media streaming. All infrastructure is orchestrated via `docker-compose.yml` at the repository root.

## Architecture — Clean Architecture (STRICT)

```text
presentation/   (routers, DTOs, presenters)  → depends on application
application/    (usecases, service interfaces) → depends on domain
domain/         (entities, repository interfaces, exceptions) → no dependencies on outer layers
infrastructure/ (ORM models, repositories, security, DI providers) → implements domain interfaces

```

### 🔴 STRICT DEPENDENCY RULES (NEVER VIOLATE)

1. **Inward Dependencies ONLY:** Outer layers can import inner layers. Inner layers MUST NEVER import outer layers.
2. **NO Infrastructure in Presentation:** The `presentation/` layer MUST NEVER import directly from `infrastructure/`.
3. **Dependency Injection:** All implementations (Repositories, Security Guards) must be defined as interfaces in `domain/` or `application/`. In `presentation/routers/`, use dependency stubs (e.g., `def stub(): raise NotImplementedError`). The actual injection MUST happen in `main.py` using FastAPI's `app.dependency_overrides`.

## Key Conventions & Standard Patterns

### 1. Standardized API Responses (Generic Envelopes)

All API endpoints MUST return responses using standardized Generic DTOs defined in `presentation/dto/base_dto.py`. NEVER return raw data arrays or objects.

- **List/GET (Paginated):** `PaginatedResponseDTO[T]` (contains `data`, `total`, `current_page`, `pages`, `is_next`, `is_prev`, `size`, `permissions`, `detail`).
- **Single/GET:** `SingleResponseDTO[T]` (contains `data`, `permissions`, `detail`).
- **Mutations (POST, PUT, PATCH, DELETE):** `MutationResponseDTO[T]` (contains `data`, `message`, `detail`).

_Implementation Rule:_ The `UseCase` returns raw domain output. The `Presenter` maps this output into the generic envelope.

### 2. Error Handling & Global Exceptions

- **Domain Layer:** Define business errors extending a `BaseAppException` (with `message` and `error_code`).
- **UseCase Layer:** Raise specific `BaseAppException` subclasses. **DO NOT** use `ValueError` or FastAPI's `HTTPException` here.
- **Presentation/Router:** **DO NOT** use `try-except` blocks in routers for business logic.
- **FastAPI / main.py:** Use global `@app.exception_handler(BaseAppException)` to catch domain errors and return a standardized `ErrorResponseDTO` (containing `success=False`, `error_code`, `message`, `details`). Swagger `responses` parameter should be used in routers to document these error models.

### 3. Security & Authentication (FastAPI Best Practices)

Use FastAPI's native `OAuth2PasswordBearer` instead of raw `HTTPBearer`/`jwt.decode` in the presentation layer.

- **Security Scheme:** Define `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")`.
- **Get Current User:** Transition from `get_current_user_id` to a complete `get_current_user` dependency that returns the authenticated `User` entity or a specific `CurrentUserDTO`.
- **DI for Auth:** To respect Clean Architecture, the router must use a stub:

```python
# presentation/router/user_router.py
def get_current_user_stub() -> User:
    raise NotImplementedError()

@router.get("/me")
def me(current_user: User = Depends(get_current_user_stub)): ...

```

The actual implementation resolving the token (parsing JWT, fetching from DB) lives in `infrastructure/security.py` or `infrastructure/auth_guard.py` and is injected in `main.py`:

```python
# main.py
app.dependency_overrides[get_current_user_stub] = real_get_current_user_from_infrastructure

```

### 4. General Code Rules

- **Naming**: `snake_case` for files/functions/variables. `PascalCase` for classes.
- **Type hints**: Required on all function signatures and dataclass/Pydantic fields.
- **Imports**: Standard library → third-party → project modules. One import per line.
- **Validation:** Use Pydantic `Field` and `@model_validator` in Request DTOs for swagger documentation and input validation.

### 5. Request & Input Validation Standards (Pydantic & Security)

The presentation layer MUST strictly validate incoming requests before they reach the Application (UseCase) layer.

- **Security (No IDOR):** NEVER include fields like `user_id`, `creator_id`, or `account_id` in a Request body DTO if that identity is derived from the authenticated user. Extract the user identity exclusively from the JWT token via the `current_user` dependency and pass it to the UseCase's `RequestInput`.
- **Rich Validation:** All `BaseModel` Request DTOs MUST use Pydantic's `Field` for primitive validation (`min_length`, `max_length`, `ge`, `regex`, etc.).
- **Cross-Field Validation:** Use `@model_validator(mode='after')` inside the Request DTO for business logic that depends on multiple fields (e.g., ensuring `end_time` is after `start_time`). Do not leave this basic validation to the UseCase.
- **Router Paths:** Pay attention to `APIRouter(prefix="/...")`. If the prefix is `/meets`, the collection endpoint is `@router.post("")` or `@router.get("")`, NOT `@router.post("/meets")`.
- **Clean Routers:** Routers must be extremely thin. They only receive the DTO, extract dependencies (User, UseCase), map them to a `RequestInput` dataclass, call the `execute` method, and pass the output to a `Presenter`. No business logic or database queries are allowed in the router.

### 6. Business Logic & Role Enforcement (RBAC)

Role-based access control (RBAC), cross-role protection, and resource ownership MUST be strictly enforced within the **UseCase layer** across the entire project.

#### A. Role Definitions & Core Constraints

- `SuperAdmin`: Globally unique (there can only be one). Ultimate power over all users and resources.
- `Admin`: High-level administrator. Can manage platform resources but has strict boundaries when interacting with other Admins or the SuperAdmin.
- `Host`: Standard meeting creator. Can only manage their own created content.
- `User`: Base participant. Registered publicly or added by admins. Has no creation capabilities.

#### B. Meeting Lifecycle Logic (Creation, Ownership, & Assignment)

All UseCases modifying meeting states (`CreateMeetUseCase`, `UpdateMeetUseCase`, `DeleteMeetUseCase`) MUST enforce these precise assignment and ownership rules:

1. **Creation & Target Assignment:**
   - **Host:** Can only create a meeting for themselves (`creator_id` MUST match their own authenticated ID).
   - **Admin:** Can create a meeting for themselves OR assign it to a `Host`. **CRITICAL:** An Admin is strictly FORBIDDEN from assigning a meeting to another `Admin` or to the `SuperAdmin`.
   - **SuperAdmin:** Can create a meeting and assign the `creator_id` to ANYONE (any Admin, Host, or themselves).

2. **Modification & Deletion (Ownership Rules):**
   - **Host:** Can ONLY update or delete meetings where they are the explicit creator (`creator_id == current_user_id`).
   - **Admin:** Can update or delete their own meetings OR meetings created by any `Host`. **CRITICAL:** An Admin MUST NEVER modify or delete meetings created by another `Admin` or the `SuperAdmin`.
   - **SuperAdmin:** Can update or delete ANY meeting across the entire platform without restriction.

#### C. User Management & Promotion Logic (Cross-Role Protections)

All UseCases handling user mutation, deletion, or role promotion/demotion MUST strictly enforce the following hierarchy:

1. **Admin Capabilities & Boundaries:**
   - Can create, edit, or delete users with `User` or `Host` roles.
   - Can promote a `User` to `Host` or `Admin`.
   - **CRITICAL BOUNDARY:** An Admin is strictly UNAUTHORIZED to edit, delete, or demote another `Admin` or the `SuperAdmin`.
2. **SuperAdmin Capabilities:**
   - Has global CRUD over all accounts.
   - Can promote, demote, or delete any `Admin`, `Host`, or `User`.
   - **CRITICAL BOUNDARY:** The `SuperAdmin` role is unique; a SuperAdmin cannot create or promote someone else to `SuperAdmin`.

#### D. Implementation Pattern in UseCases

- These checks MUST happen at the very beginning of the UseCase's `execute()` method.
- Fetch both the actor (current authenticated user) and the target resource/user from repositories to perform hierarchy comparisons.
- If a rule is breached, raise a specific domain exception extending `BaseAppException` (e.g., `UnauthorizedRoleError`, `ForbiddenActionError`, or `RoleHierarchyViolationError`). Do NOT leak HTTP concepts here; the presentation layer handler will translate these to `403 Forbidden`.

#### E. View/Access Rules (Queries)

All GET endpoints returning meeting data MUST enforce role-based filtering:

1. **SuperAdmin:** Can view ANY meeting in the system. Full visibility and no filtering restrictions.
2. **Admin:** Can view ANY meeting in the system. No access restrictions on queries.
3. **Host:** Can view meets they created (`creator_id == actor_id`) OR meets they are invited to (actor_id in `participants_ids`).
4. **User:** Can view ONLY meets they are explicitly invited to as a participant. Cannot view meets they did not create and are not part of.

_Implementation rule:_ Apply the filtering logic at the repository query level to avoid loading unauthorized data. The `ListMeetsUseCase` MUST receive the actor's role and ID, then build the appropriate query filter.

#### F. Response Envelope Requirements

All API responses MUST use the generic envelopes from `presentation/dto/base_dto.py`:

| Endpoint Type | Envelope | Fields |
|---------------|----------|--------|
| **Mutations** (POST, PUT, PATCH, DELETE) | `MutationResponseDTO[T]` | `data: T`, `message: str`, `detail: Optional[str]` |
| **Single Item GET** | `SingleResponseDTO[T]` | `data: T`, `permissions: list[str]`, `detail: Optional[str]` |
| **Paginated List GET** | `PaginatedResponseDTO[T]` | `data: list[T]`, `total: int`, `current_page: int`, `pages: int`, `is_next: bool`, `is_prev: bool`, `size: int`, `permissions: list[str]`, `detail: Optional[str]` |

_Implementation rule:_ The UseCase returns raw domain output. The `Presenter` maps this output into the correct generic envelope. Never return raw lists or bare objects from endpoints.

### 7. LiveKit Infrastructure (Docker Sidecar)

LiveKit is the WebRTC media server powering all real-time audio/video streaming.

- **Role**: LiveKit handles the media plane (SFU, selective forwarding unit). The FastAPI backend never handles raw media streams.
- **JWT Tokens**: FastAPI generates LiveKit access tokens for authenticated users. These tokens grant permission to join specific rooms. The actual join and media exchange happens directly between the client and LiveKit over WebSocket.
- **Orchestration**: LiveKit runs as a Docker container defined in `docker-compose.yml` alongside the `api` and `db` services. Configuration is mounted from `livekit.yaml` at the repository root.
- **Ports**:
  - `7880` — WebSocket signal port (client ↔ LiveKit)
  - `7882` — UDP/TCP media port (media relay)
- **Keys**: The `devkey` / `devsecret` pair in `livekit.yaml` must match `LIVEKIT_API_KEY` / `LIVEKIT_API_SECRET` in the FastAPI environment for token verification.

## Commands

| Action               | Command                                                   |
| -------------------- | --------------------------------------------------------- |
| Build & start stack  | `docker-compose up -d --build`                            |
| Stop stack           | `docker-compose down`                                     |
| View api logs        | `docker-compose logs -f api`                              |
| Shell into api       | `docker-compose exec api /bin/sh`                         |
| Create migration     | `docker-compose exec api alembic revision --autogenerate -m "description"` |
| Apply migrations     | `docker-compose exec api alembic upgrade head`             |
| Rollback one         | `docker-compose exec api alembic downgrade -1`             |
| Run server (local)   | `uvicorn main:app --reload`                               |
| Install deps (local) | `pip install -r requirements.txt`                         |

## Common Pitfalls (AI Assistant Checklist)

- **DO NOT** add `message` or framework-specific fields directly to Domain or UseCase models. They belong in Presenters/DTOs.
- No existing tests — any new feature must be modular enough to be testable.
- Pydantic v2: `@model_validator(mode='after')` returns `self`, not the whole class. Always use `mode='after'` for multi-field validation.

## Project Structure

```text
meeting/
├── AGENTS.md ← project conventions & known pitfalls
├── README.md
├── main.py ← FastAPI composition root (global exception handler, DI overrides)
├── Dockerfile ← multi-stage, non-root user
├── requirements.txt
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/
│       ├── 04d41407227e_add_remove_user_fields.py
│       ├── 97717f8d0e39_add_remove_user_fields.py
│       ├── ffa7f9c8af57_update_user_role_enum.py
│       └── 6a1b2c3d4e5f_add_superadmin_role_to_user_enum.py
├── .agents/skills/
│   ├── clean-architecture/
│   └── fastapi-python/
├── domain/
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── base_exceptions.py ← BaseAppException + 6 derived domain exceptions
│   ├── entity/
│   │   ├── meet_entity.py ← Meet entity with domain logic
│   │   └── user_entity.py ← Role includes SuperAdmin, Admin, Host, User
│   └── repository_interface/
│       ├── meet_repository_interface.py
│       ├── participant_repository_interface.py
│       ├── refresh_token_repository_interface.py
│       └── user_repository_interface.py
├── application/usecases/
│   ├── create_meet_usecase.py ← RBAC-enforced, domain exceptions
│   ├── delete_meet_usecase.py ← ownership & hierarchy checks
│   ├── get_meet_by_hash_usecase.py ← role-based view access
│   ├── get_user_usecase.py
│   ├── list_meets_usecase.py ← paginated, role-filtered
│   ├── list_user_invitations_usecase.py ← participant meets
│   ├── list_user_managed_meets_usecase.py ← creator meets
│   ├── login_user_usecase.py
│   ├── logout_user_usecase.py
│   ├── refresh_token_usecase.py
│   ├── register_user_usecase.py
│   └── update_meet_usecase.py ← assignment logic, RBAC
├── infrastructure/
│   ├── database.py
│   ├── security.py ← env var for SECRET_KEY
│   ├── auth_guard.py ← OAuth2PasswordBearer, returns full User entity
│   ├── orm/
│   │   ├── meet_model.py
│   │   ├── participant_model.py
│   │   ├── refresh_token_model.py
│   │   └── user_model.py ← Role enum includes SuperAdmin
│   ├── repository/
│   │   ├── postgres_meet_repository.py
│   │   ├── postgres_refresh_token_repository.py
│   │   └── postgres_user_repository.py
│   └── provider/
│       ├── meet_provider.py
│       └── user_provider.py
└── presentation/
    ├── dto/
    │   ├── base_dto.py ← MutationResponseDTO[T], SingleResponseDTO[T], PaginatedResponseDTO[T], ErrorResponseDTO
    │   ├── create_meet_dto.py ← No IDOR, Field validations, model_validator, MeetResponseData
    │   ├── get_user_dto.py
    │   ├── login_user_dto.py
    │   ├── refresh_token_dto.py
    │   └── register_user_dto.py
    ├── presenter/
    │   ├── meet_presenter.py ← wraps in MutationResponseDTO
    │   └── user_presenter.py ← wraps in MutationResponseDTO
    ├── dependencies/
    │   └── auth_stub.py ← get_current_user_stub + oauth2_scheme (centralized)
    └── router/
        ├── meet_router.py ← thin, no try-except, no business logic
        └── user_router.py ← thin, imports get_current_user_stub, no try-except

```

## Git commit

When I say `git commit` please do the following:

```text
Please act as an expert Git commit assistant. Your task is to carefully review the recent project changes (e.g., via git diff or staged files) and generate a series of clear, conventional commit messages following best practices. Use Gitmoji emojis at the start of each commit message to make them more expressive and readable (e.g., :sparkles: for new features, :bug: for fixes).
Key guidelines:
Conventional structure: Each commit message should start with a Gitmoji, followed by a type (e.g., feat, fix, refactor, docs, test, chore), a scope in parentheses if applicable (e.g., (ui)), a colon, and a concise description. Include a body if needed for more details, and reference issues if relevant.
Grouping: Break changes into logical, atomic commits. Group related files or changes together (e.g., one commit for UI updates, another for bug fixes), rather than lumping everything into a single commit. Avoid overly large or unrelated groupings.
Execution: Directly output and execute the necessary Git shell commands (e.g., git add for specific files, followed by git commit -m "message") to apply these commits. Do not ask for confirmation, additional input, or perform unrelated actions like rebasing, squashing, or amending existing commits. Only create new commits on the current branch.
Best practices: Ensure messages are imperative, concise (50 chars for subject), and descriptive. Focus on what changed and why, not how.
Additional notes:
- Use present tense for the subject line (e.g., "Add feature" not "Added feature")
- Be specific about what was changed (e.g., "Fix user login validation" rather than just "Fix bug")
- When making breaking changes, indicate this with an exclamation mark after the type (e.g., "feat!: Remove deprecated API endpoint")
- Reference issue numbers if applicable (e.g., "fix(auth): Resolve login issue #123")
- For multiple related changes, create separate commits for each logical change
- When updating dependencies, mention the specific packages (e.g., "chore(deps): Update react and react-dom to v18")
- For documentation changes, be clear about what documentation was added or updated
- When changing configuration files, explain the purpose of the changes
Proceed step-by-step: First, analyze the changes, then propose the grouped commits, and finally execute the Git commands in sequence.

```
