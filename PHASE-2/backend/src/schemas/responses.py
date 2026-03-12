from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T
    message: str | None = None


class ErrorDetail(BaseModel):
    field: str
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: list[ErrorDetail] | None = None
    code: str


class DeleteResponse(BaseModel):
    success: bool = True
    message: str
