# Base stage
FROM python:3.11-slim-bullseye as base
ARG BUILD_ENV
ARG UID=1000
ARG GID=1000
ENV PATH="/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
RUN groupadd -g "${GID}" -r appuser && \
    useradd -d "/app" -g appuser -r -u "${UID}" appuser && \
    mkdir -p "/var/www/django/static" "/var/www/django/media" && \
    chown -R appuser:appuser "/app" "/var/www/django/static" "/var/www/django/media"
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gettext

# Builder stage
FROM base as builder
ENV POETRY_VERSION=1.3.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential
RUN python -m venv /venv && \
    python -m pip install poetry==${POETRY_VERSION}
COPY --chown=appuser:appuser pyproject.toml poetry.lock /app/
RUN poetry install $(test "$BUILD_ENV" = "production" && echo "--only main") --no-ansi --no-interaction --no-root

# Development stage
FROM base as dev
EXPOSE 8000
COPY --from=builder --chown=appuser:appuser /venv /venv
COPY ./docker/django/entrypoint.sh /docker-entrypoint.sh
RUN chmod +x "/docker-entrypoint.sh"
USER appuser
ENTRYPOINT ["/docker-entrypoint.sh"]

# Production stage
FROM dev as prod
COPY --chown=appuser:appuser . /app/