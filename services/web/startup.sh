#!/bin/bash
#alembic upgrade head
if [ "$PRODUCTION" = true ]; then
source .env
gunicorn bin.setup:setup_app -w 4 -k uvicorn.workers.UvicornWorker -b $SERVER_HOST:$SERVER_PORT
else
python -m debugpy --wait-for-client --listen $SERVER_HOST:5678 -m uvicorn --factory bin.setup:setup_app --reload --host $SERVER_HOST --port $SERVER_PORT --lifespan on --log-level debug
fi