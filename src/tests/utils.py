from datetime import date
from uuid import uuid4

from domain.entities.employee import Employee
from domain.entities.salary import Salary
from domain.value_objects.price import Price, CurrencyOption


def create_salary(
    employee_id: uuid4,
    rate_per_hour_value: float = 10.0,
    rate_per_hour_currency: CurrencyOption = CurrencyOption.euro,
    bonus_value: float = 0.0,
    bonus_currency: CurrencyOption = CurrencyOption.euro,
    date_: date | None = None,
    hours_worked: float = 0.0
) -> Salary:
    return Salary(
        employee_id=employee_id,
        rate_per_hour=Price(value=rate_per_hour_value, currency=rate_per_hour_currency),
        bonus=Price(value=bonus_value, currency=bonus_currency),
        date=date.today() if not date_ else date_,
        hours_worked=hours_worked
    )


def create_employee(
    name: str = "Test Employee",
    min_rate_per_hour_value: float = 10.0,
    min_rate_per_hour_currency: CurrencyOption = CurrencyOption.euro,
    is_active: bool = True,
    rate_per_hour_value: float = 10.0,
    rate_per_hour_currency: CurrencyOption = CurrencyOption.euro,
) -> Employee:
    return Employee(
        name=name,
        min_rate_per_hour=Price(
            value=min_rate_per_hour_value, currency=min_rate_per_hour_currency
        ),
        is_active=is_active,
        rate_per_hour=Price(
            value=rate_per_hour_value, currency=rate_per_hour_currency
        ),
    )
