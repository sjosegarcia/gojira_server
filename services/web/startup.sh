#!/bin/bash
alembic upgrade head
if [ "$ENV" = "PRODUCTION" ]; then
source .env.prod
gunicorn setup.start_app:start_app -t 0 -w 1 -k uvicorn.workers.UvicornWorker -b $HOST:$PORT --threads 8 --log-level debug --forwarded-allow-ips="*"
else
python -m debugpy --wait-for-client --listen $HOST:5678 -m uvicorn --factory setup.start_app:start_app --reload --host $HOST --port $PORT --lifespan on --log-level debug --forwarded-allow-ips '*' --workers 1
fi