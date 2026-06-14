from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")


class MutationResponseDTO(BaseModel, Generic[T]):
    data: T
    message: str
    detail: Optional[str] = None


class SingleResponseDTO(BaseModel, Generic[T]):
    data: T
    permissions: list[str] = []
    detail: Optional[str] = None


class PaginatedResponseDTO(BaseModel, Generic[T]):
    data: list[T]
    total: int
    current_page: int
    pages: int
    is_next: bool
    is_prev: bool
    size: int
    permissions: list[str] = []
    detail: Optional[str] = None


class ErrorResponseDTO(BaseModel):
    success: bool = False
    error_code: str
    message: str
    details: Optional[dict] = None
