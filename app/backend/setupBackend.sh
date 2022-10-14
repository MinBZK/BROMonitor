#!/bin/sh
gunicorn main:app -w 5 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000