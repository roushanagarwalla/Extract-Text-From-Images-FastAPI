#!/bin/bash

RUN_PORT=${PORT:-8000}

gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind "0.0.0.0:${RUN_PORT}"