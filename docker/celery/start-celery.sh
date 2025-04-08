#!/bin/bash

set -o errexit
set -o nounset

exec celery -A gs_tools_django.celery worker -l INFO --pool=prefork --concurrency=1 --max-tasks-per-child=1