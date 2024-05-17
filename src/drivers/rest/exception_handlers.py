from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from use_cases.exceptions import (
    EmployeeNotFoundError,
    EmployeeNotActiveError,
    SalaryError,
)
from adapters.exceptions import ExternalError


def exception_container(app: FastAPI) -> None:
    @app.exception_handler(EmployeeNotFoundError)
    async def employee_not_found_exception_handler(
            request: Request, exc: EmployeeNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)}
        )

    @app.exception_handler(EmployeeNotActiveError)
    async def employee_not_active_exception_handler(
            request: Request, exc: EmployeeNotActiveError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": str(exc)},
        )

    @app.exception_handler(SalaryError)
    async def salary_exception_handler(
            request: Request, exc: SalaryError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": str(exc)},
        )

    @app.exception_handler(ExternalError)
    async def external_exception_handler(
            request: Request, exc: ExternalError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Something went wrong. Please try again"},
        )
