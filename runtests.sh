#!/bin/bash
set -e

python -m coverage erase
python -m pytest --cov=behave_web_api --cov-report=term-missing
nohup python testserver.py & echo $! > run.pid
trap "kill \$(cat run.pid)" EXIT
sleep 3
BASE_URL=localhost:5000 python -m coverage run --append -m behave features/requests.feature
python -m coverage report -m
