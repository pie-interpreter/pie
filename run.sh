#!/bin/bash

# Launcher for pie from command line (action simplifier)
# It supposes that PYPY is situated in the directory '../pypy'
# sery0ga

PYTHONPATH=${PYTHONPATH}:../pypy:. python pie/main.py $1