#!/bin/bash

export FLASK_APP=python/server/app.py
export PYTHONPATH=$PYTHONPATH:$ROOT/python

python -m flask run $@

