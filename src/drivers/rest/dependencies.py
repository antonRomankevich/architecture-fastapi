from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from adapters.repositories.employee_repository.mongodb_repository import (
    MongoEmployeeRepository,
)
from ports.repositories.employee_repository import EmployeeRepository
from use_cases.submit_salary_use_case import SubmitSalaryUseCase


@lru_cache
def get_mongo_client() -> AsyncIOMotorClient:  # type: ignore
    return AsyncIOMotorClient("mongodb://localhost:27017")


def get_employee_repository(
        mongo_client: Annotated[AsyncIOMotorClient, Depends(get_mongo_client)],  # type: ignore
) -> EmployeeRepository:
    return MongoEmployeeRepository(mongo_client)


def get_submit_salary_use_case(
        employee_repository: Annotated[EmployeeRepository, Depends(get_employee_repository)],
) -> SubmitSalaryUseCase:
    return SubmitSalaryUseCase(employee_repository)
