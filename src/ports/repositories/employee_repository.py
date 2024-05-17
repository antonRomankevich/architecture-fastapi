from abc import ABC, abstractmethod
from typing import Any

from domain.entities.employee import Employee
from domain.entities.salary import Salary


class EmployeeRepository(ABC):
    @abstractmethod
    async def get(self, **filters: Any) -> Employee | None:
        pass

    @abstractmethod
    async def add_salary(self, salary: Salary) -> bool:
        pass
