#!/bin/bash

# Launcher for pie coverage tests from command line (action simplifier)
# It supposes that PYPY is situated in the directory '../pypy'

PYTHONPATH=${PYTHONPATH}:../pypy:. python run_tests.py