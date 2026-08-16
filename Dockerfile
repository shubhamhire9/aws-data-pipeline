# Dockerfile
FROM python:3.10-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get purge -y --auto-remove curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# Install production dependencies only (skip dev)
RUN poetry install --no-dev --no-root --no-interaction --no-ansi

COPY . .

# Install the project itself (production only)
RUN poetry install --no-dev --no-interaction --no-ansi

RUN python -c "import etl; print('ETL package installed')"

ENTRYPOINT ["python", "-m", "etl.pipeline"]