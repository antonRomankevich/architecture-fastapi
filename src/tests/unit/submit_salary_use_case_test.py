import uuid

import pytest

from adapters.repositories.employee_repository.in_memory_repository import (
    InMemoryEmployeeRepository,
)
from domain.value_objects.price import Price, CurrencyOption
from ports.repositories.employee_repository import EmployeeRepository
from tests.utils import create_employee, create_salary
from use_cases.exceptions import (
    EmployeeNotFoundError,
    EmployeeNotActiveError,
    SalaryError,
)
from use_cases.submit_salary_use_case import SubmitSalaryUseCase


@pytest.fixture
def employee_repository() -> EmployeeRepository:
    return InMemoryEmployeeRepository()


@pytest.fixture
def submit_salary_use_case(employee_repository: EmployeeRepository) -> SubmitSalaryUseCase:
    return SubmitSalaryUseCase(employee_repository)


async def test_employee_not_found(submit_salary_use_case: SubmitSalaryUseCase):
    salary = create_salary(employee_id=uuid.uuid4())
    with pytest.raises(EmployeeNotFoundError):
        await submit_salary_use_case(salary)


async def test_employee_not_active(
        employee_repository: InMemoryEmployeeRepository,
        submit_salary_use_case: SubmitSalaryUseCase,
):
    employee = create_employee()
    employee.is_active = False
    employee_repository.employees.append(employee)
    salary = create_salary(employee_id=employee.id)
    with pytest.raises(EmployeeNotActiveError):
        await submit_salary_use_case(salary)


async def test_salary_invalid_rate_per_hour(
        employee_repository: InMemoryEmployeeRepository,
        submit_salary_use_case: SubmitSalaryUseCase,
):
    employee = create_employee()
    employee.min_rate_per_hour = Price(value=15, currency=CurrencyOption.euro)  # Update to Price instance
    employee_repository.employees.append(employee)
    salary = create_salary(employee_id=employee.id, rate_per_hour_value=10)
    with pytest.raises(SalaryError):
        await submit_salary_use_case(salary)


async def test_salary_successfully_added(
        employee_repository: InMemoryEmployeeRepository,
        submit_salary_use_case: SubmitSalaryUseCase,
):
    employee = create_employee()
    employee_repository.employees.append(employee)
    salary = create_salary(employee_id=employee.id)
    await submit_salary_use_case(salary)
    result = await employee_repository.get(id=employee.id)
    assert result is not None and salary in result.salaries
