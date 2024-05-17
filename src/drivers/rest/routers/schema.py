from uuid import UUID
from datetime import date

from pydantic import BaseModel

from domain.entities.salary import Salary
from domain.value_objects.price import CurrencyOption, Price


class PriceInput(BaseModel):
    value: float
    currency: CurrencyOption

    def to_entity(self) -> Price:
        return Price(value=self.value, currency=self.currency)


class SalaryInput(BaseModel):
    employee_id: UUID
    price: PriceInput

    def to_entity(self) -> Salary:
        return Salary(
            employee_id=self.employee_id,
            rate_per_hour=self.price.to_entity(),
            hours_worked=0,
            bonus=Price(value=0, currency=self.price.currency),
            date=date.today(),
        )
