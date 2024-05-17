from ports.repositories.employee_repository import EmployeeRepository
from use_cases.exceptions import (
    EmployeeNotActiveError,
    SalaryError,
    EmployeeNotFoundError,
)
from domain.entities.salary import Salary


class SubmitSalaryUseCase:
    def __init__(self, employee_repository: EmployeeRepository):
        self._employee_repository = employee_repository

    async def __call__(self, salary: Salary) -> None:
        employee = await self._employee_repository.get(id=salary.employee_id)
        if not employee:
            raise EmployeeNotFoundError(salary.employee_id)
        if not employee.is_active:
            raise EmployeeNotActiveError(employee.id)
        if salary.rate_per_hour.value < employee.min_rate_per_hour.value:
            raise SalaryError(employee.min_rate_per_hour)
        await self._employee_repository.add_salary(salary)
