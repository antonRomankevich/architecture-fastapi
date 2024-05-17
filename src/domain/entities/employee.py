from dataclasses import dataclass, field
from uuid import UUID, uuid4

from domain.entities.salary import Salary
from domain.value_objects.price import Price, CurrencyOption


@dataclass
class Employee:
    name: str
    rate_per_hour: Price
    min_rate_per_hour: Price
    is_active: bool = True
    salaries: list[Salary] = field(default_factory=list)
    bonuses: list[Salary] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)

    def calculate_total_salary(self) -> Price:
        total_value = sum(salary.total_salary.value for salary in self.salaries)
        currency = self.rate_per_hour.currency if self.salaries else CurrencyOption.dollar
        return Price(value=total_value, currency=currency)

    def add_salary(self, salary: Salary):
        self.salaries.append(salary)
