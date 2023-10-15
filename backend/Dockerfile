FROM python:3.11.3 as base

ENV POETRY_VERSION=1.4.2 \
  PATH="/root/.local/bin:$PATH"

# Install poetry: # https://python-poetry.org/docs/master/#installation
RUN apt-get update && \
  apt-get install -y curl && \
  curl -sSL https://install.python-poetry.org | python3 - --version "$POETRY_VERSION" && \
  poetry config virtualenvs.create false

#############################################
FROM base as dev

EXPOSE 5000
WORKDIR /app
COPY  poetry.lock* pyproject.toml ./
RUN poetry install --no-interaction
COPY . /app

#############################################
FROM base as prod

WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction --no-dev
COPY . /app

CMD ["sh","-c","alembic upgrade head && uvicorn api.main:app --host 0.0.0.0 --port 5000"]

