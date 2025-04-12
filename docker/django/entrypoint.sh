#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

postgres_ready() {
python <<END
import sys
import psycopg
try:
    psycopg.connect(
        dbname="${GSTOOLS_POSTGRES_DB}",
        user="${GSTOOLS_POSTGRES_USER}",
        password="${GSTOOLS_POSTGRES_PASSWORD}",
        host="${GSTOOLS_POSTGRES_HOST-db}",
        port="${GSTOOLS_POSTGRES_PORT-5432}",
    )
except psycopg.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
        echo >&2 'Waiting for PostgreSQL to become available...'
        sleep 1
done
echo >&2 'PostgreSQL is available'

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000
# python manage.py compilemessages

exec "$@"