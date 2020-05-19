#!/bin/bash

#Build => Test => Coverage
pip install coverage
coverage run setup.py test
coverage report -m
coverage html
echo "Open htmlcov/index.html"