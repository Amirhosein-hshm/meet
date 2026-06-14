from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Request

from domain.exceptions.base_exceptions import BaseAppException
from infrastructure.database import Base, engine
from presentation.dto.base_dto import ErrorResponseDTO
from presentation.router.user_router import router as user_router
from presentation.router.meet_router import router as meet_router
from infrastructure.provider.user_provider import register_user_di
from infrastructure.provider.meet_provider import register_meet_di


app = FastAPI(
    title="Meeting Project Management System",
    description="Clean Architecture implementation with FastAPI",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(meet_router)
register_user_di(app)
register_meet_di(app)


@app.exception_handler(BaseAppException)
async def domain_exception_handler(request: Request, exc: BaseAppException):
    status_map = {
        "UNAUTHORIZED_ROLE": 403,
        "FORBIDDEN_ACTION": 403,
        "ROLE_HIERARCHY_VIOLATION": 403,
        "INVALID_PARTICIPANT": 400,
        "NOT_FOUND": 404,
        "CONFLICT": 409,
        "GENERIC_ERROR": 400,
    }
    status_code = status_map.get(exc.error_code, 400)
    return JSONResponse(
        status_code=status_code,
        content=ErrorResponseDTO(
            success=False,
            error_code=exc.error_code,
            message=exc.message,
            details=None,
        ).model_dump(),
    )
