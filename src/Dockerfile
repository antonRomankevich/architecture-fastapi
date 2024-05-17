FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN poetry install

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "drivers.rest.main:app", "--host", "0.0.0.0", "--port", "8000"]
