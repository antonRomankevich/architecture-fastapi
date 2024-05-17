from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from drivers.rest.dependencies import get_submit_salary_use_case
from drivers.rest.routers.schema import SalaryInput
from use_cases.submit_salary_use_case import SubmitSalaryUseCase

router = APIRouter(prefix="/employees")


@router.post("/{employee_id}/salaries", status_code=status.HTTP_204_NO_CONTENT)
async def submit_salary(
        employee_id: UUID,
        data: SalaryInput,
        use_case: Annotated[SubmitSalaryUseCase, Depends(get_submit_salary_use_case)],
) -> None:
    await use_case(data.to_entity(employee_id))
