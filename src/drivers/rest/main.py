from fastapi import FastAPI

from drivers.rest.exception_handlers import exception_container
from drivers.rest.routers import employee

app = FastAPI()

app.include_router(employee.router)

exception_container(app)
