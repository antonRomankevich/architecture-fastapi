from typing import Any

from domain.entities.employee import Employee
from domain.entities.salary import Salary
from ports.repositories.employee_repository import EmployeeRepository


class InMemoryEmployeeRepository(EmployeeRepository):
    employees: list[Employee] = []

    async def get(self, **filters: Any) -> Employee | None:
        for employee in self.employees:
            if (f := filters.get("id")) and f == employee.id:
                return employee
        return None

    async def add_salary(self, salary: Salary) -> bool:
        for employee in self.employees:
            if employee.id == salary.employee_id:
                employee.salaries.append(salary)
                return True
        return False

    async def add(self, employee: Employee) -> None:
        self.employees.append(employee)
