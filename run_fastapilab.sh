#!/bin/sh
# fastapi startup shell script

uvicorn fastapilab.main:app --proxy-headers --host 0.0.0.0 --port 8000


