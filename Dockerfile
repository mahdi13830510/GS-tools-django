# ┌──────────┐
# │Base Image│
# └──────────┘
FROM focker.ir/python:3.11.4-slim-bullseye as base

ARG BUILD_ENV \
    UID=1000 \
    GID=1000

ENV PATH="/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PYTHONFAULTHANDLER=1

WORKDIR /app

# create a non-root user
RUN <<EOF
# create user and group
groupadd -g "${GID}" -r appuser
useradd -d "/app" -g appuser -l -r -u "${UID}" appuser
# static and media files
mkdir -p "/var/www/django/static" "/var/www/django/media"
# set appuser as owner
chown -R appuser:appuser "/app" "/var/www/django/static" "/var/www/django/media"
EOF

RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt/lists <<EOF
# don't delete downloaded packages so they can be cached
rm -f /etc/apt/apt.conf.d/docker-clean
# install packages
apt-get update
apt-get install -y --no-install-recommends libpq-dev gettext
EOF

# ┌────────────────────────┐
# │Dependency Builder Image│
# └────────────────────────┘
FROM base as builder

ENV BUILD_ENV=${BUILD_ENV} \
    # pip:
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=1.3.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_OPTIONS_NO_PIP=true \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt/lists <<EOF
# install packages
apt-get update
apt-get install -y --no-install-recommends build-essential
EOF

# install poetry
RUN --mount=type=cache,target=/root/.cache <<EOF
# create a new venv(using system python). after this, since /venv comes
# first in the PATH, running python will use the venv python.
python -m venv /venv
# we need to populate the venv with our dependencies so we can copy them
# inside the dev image. poetry will use the python that it was installed
# with, which is our vevn python in this case.
python -m pip install poetry==${POETRY_VERSION} # this is the venv python
EOF

# copy poetry files
COPY --chown=appuser:appuser pyproject.toml poetry.lock README.md /app/

# install dependencies
RUN --mount=type=cache,target="$POETRY_CACHE_DIR" <<EOF
poetry install $(test "$BUILD_ENV" = "production" && echo "--only main") --no-ansi --no-interaction --no-root
EOF

# ┌─────────────────┐
# │Development Image│
# └─────────────────┘
FROM base as dev

EXPOSE 8000

COPY --from=builder --chown=appuser:appuser /venv /venv

COPY ./docker/django/entrypoint.sh /docker-entrypoint.sh
COPY ./docker/celery/start-celery.sh /start-celery.sh

RUN chmod +x "/docker-entrypoint.sh" "/start-celery.sh"

USER appuser

ENTRYPOINT ["/docker-entrypoint.sh"]

# ┌────────────────┐
# │Production Image│
# └────────────────┘
FROM dev as prod

COPY --chown=appuser:appuser . .