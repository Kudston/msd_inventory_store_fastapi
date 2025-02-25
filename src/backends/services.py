from functools import lru_cache
from typing import Any, Generic, TypeVar
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import FastAPI
from config import Settings
from fastapi.openapi.utils import get_openapi
from exceptions import (
    GeneralException,
    handle_bad_request_exception,
    handle_conflict_exception,
    handle_forbidden_exception,
    handle_not_found_exception,
    handle_file_too_large_exception,
)

from users import schemas

_T = TypeVar("_T")


@lru_cache()
def get_settings():
    return Settings()


def does_admin_token_match(token):
    return (
        token is not None and get_settings().admin_signup_token.lower() == token.lower()
    )


class AppResponseModel(BaseModel):
    detail: str


class ServiceResult(Generic[_T]):
    def __init__(
        self, data: Any, success: bool, message: str = "", exception: Exception = None  # type: ignore
    ) -> None:
        self.data = data
        self.success = success
        self.message = message
        self.exception = exception

    def __str__(self) -> str:
        if self.success:
            return self.data
        else:
            return f"Exception: {self.exception.__str__()}"


class BaseService:
    def __init__(self, requesting_user: schemas.UserOut, db: Session) -> None:
        self.requesting_user = requesting_user
        self.db = db


def success_service_result(data: Any):
    return ServiceResult(data=data, success=True, exception=None)  # type: ignore


def failed_service_result(exception: Exception):  # type: ignore
    return ServiceResult(data=None, success=False, exception=exception)  # type: ignore


def handle_result(result: ServiceResult, expected_schema: BaseModel = None):  # type: ignore
    """Handles the result returned from any service in the application, both failures and successes."""

    if result.success:
        try:
            if expected_schema is not None:
                return expected_schema.model_validate(result.data)
            else:
                return AppResponseModel(detail=result.data)
        except Exception as raised_exception:
            handle_bad_request_exception(raised_exception)

    if isinstance(result.exception, GeneralException):
        handle_bad_request_exception(result.exception)
    else:
        handle_bad_request_exception(result.exception)
