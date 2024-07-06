#!/usr/bin/env bash

python -m gunicorn --bind 0.0.0.0:10808 main:application &
python bot.py