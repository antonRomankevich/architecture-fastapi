from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID, uuid4

from domain.value_objects.price import Price


@dataclass
class Salary:
    employee_id: UUID
    rate_per_hour: Price
    hours_worked: float
    bonus: Price
    date: date
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def total_salary(self) -> Price:
        total_value = (self.rate_per_hour.value * self.hours_worked) + self.bonus.value
        return Price(value=total_value, currency=self.rate_per_hour.currency)
