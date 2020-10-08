#!/bin/bash

python -u -m "muzeeglot.ingest"

GUNICORN_OPTS="${GUNICORN_OPTS} --workers=4"
GUNICORN_OPTS="${GUNICORN_OPTS} --bind=0.0.0.0:80"
GUNICORN_OPTS="${GUNICORN_OPTS} --worker-class=uvicorn.workers.UvicornWorker"

gunicorn $GUNICORN_OPTS "muzeeglot:api"