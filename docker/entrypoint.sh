#!/bin/sh

if [ "$1" = "debug" ]; then
    poetry run uvicorn --reload user_chat.app.main:app --port 8081 --host 0.0.0.0
elif [ "$1" = "run" ]; then
    uvicorn --workers "${UVICORN_WORKERS:=4}" user_chat.app.main:app --port 8081
else
    echo "Usage:
    $0 (run|debug)"
    exit 1
fi
