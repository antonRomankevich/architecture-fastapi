from uuid import UUID
from domain.value_objects.price import Price


class EmployeeNotFoundError(Exception):
    def __init__(self, employee_id: UUID):
        self.employee_id = employee_id

    def __str__(self) -> str:
        return f"Employee not found: {self.employee_id}"


class EmployeeNotActiveError(Exception):
    def __init__(self, employee_id: UUID):
        self.employee_id = employee_id

    def __str__(self) -> str:
        return f"Employee is not active: {self.employee_id}"


class SalaryError(Exception):
    def __init__(self, min_rate_per_hour: Price):
        self.min_rate_per_hour = min_rate_per_hour

    def __str__(self) -> str:
        return f"Salary rate per hour should be higher than {self.min_rate_per_hour.value} {self.min_rate_per_hour.currency}"
