#!/bin/bash

if [[ "$WEBHOOK" == "true" ]]; then
  gunicorn main:init_func --bind 0.0.0.0:8080 --worker-class aiohttp.GunicornWebWorker
else
  python3 main.py
fi