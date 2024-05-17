from datetime import date, datetime
from typing import Any, Optional
from uuid import UUID

from adapters.exceptions import DatabaseError
from domain.entities.employee import Employee
from domain.entities.salary import Salary
from domain.value_objects.price import Price
from ports.repositories.employee_repository import EmployeeRepository
from motor.motor_asyncio import AsyncIOMotorClient
from bson import Binary


class MongoEmployeeRepository(EmployeeRepository):
    def __init__(self, client: AsyncIOMotorClient):
        self.collection = client.employees.employee

    async def get(self, id: UUID) -> Optional[Employee]:
        try:
            document = await self.collection.find_one({"_id": Binary(id.bytes)})
            return self.__to_employee_entity(document) if document else None
        except Exception as e:
            raise DatabaseError(e)

    async def add_salary(self, salary: Salary) -> bool:
        try:
            result = await self.collection.update_one(
                {"_id": Binary(salary.employee_id.bytes)},
                {"$push": {"salaries": self.__salary_to_doc(salary)}},
            )
            return bool(result.modified_count)
        except Exception as e:
            raise DatabaseError(e)

    async def add(self, employee: Employee) -> None:
        try:
            employee_doc = self.__employee_to_doc(employee)
            await self.collection.insert_one(employee_doc)
        except Exception as e:
            raise DatabaseError(e)

    def __employee_to_doc(self, employee: Employee) -> dict[str, Any]:
        return {
            "_id": Binary(employee.id.bytes),
            "name": employee.name,
            "rate_per_hour": self.__price_to_dict(employee.rate_per_hour),
            "bonuses": [self.__price_to_dict(bonus) for bonus in employee.bonuses],
            "salaries": [self.__salary_to_doc(salary) for salary in employee.salaries],
        }

    def __salary_to_doc(self, salary: Salary) -> dict[str, Any]:
        return {
            "_id": Binary(salary.id.bytes),
            "employee_id": Binary(salary.employee_id.bytes),
            "rate_per_hour": self.__price_to_dict(salary.rate_per_hour),
            "hours_worked": salary.hours_worked,
            "bonus": self.__price_to_dict(salary.bonus),
            "date": salary.date.isoformat(),
            "created_at": salary.created_at.isoformat(),
        }

    def __price_to_dict(self, price: Price) -> dict[str, Any]:
        return {"value": price.value, "currency": price.currency.value}

    def __to_employee_entity(self, obj: dict[str, Any]) -> Employee:
        return Employee(
            id=UUID(bytes=obj["_id"]),
            name=obj["name"],
            rate_per_hour=Price(**obj["rate_per_hour"]),
            bonuses=[Price(**bonus) for bonus in obj["bonuses"]],
            salaries=[self.__to_salary_entity(salary) for salary in obj["salaries"]],
        )

    def __to_salary_entity(self, salary: dict[str, Any]) -> Salary:
        return Salary(
            id=UUID(bytes=salary["_id"]),
            employee_id=UUID(bytes=salary["employee_id"]),
            rate_per_hour=Price(**salary["rate_per_hour"]),
            hours_worked=salary["hours_worked"],
            bonus=Price(**salary["bonus"]),
            date=date.fromisoformat(salary["date"]),
            created_at=datetime.fromisoformat(salary["created_at"]),
        )
