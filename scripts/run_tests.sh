#!/bin/bash

BASEDIR="$( cd "$( dirname "$0" )" && pwd )"

#Build => Test => Coverage
pip install coverage
coverage run setup.py test
coverage xml -o $BASEDIR/../cobertura-coverage.xml