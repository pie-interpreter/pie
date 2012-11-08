#!/bin/bash

# Simple pie compiler
# It supposes that PYPY is situated in the directory '../pypy'
# sery0ga

PYTHONPATH=${PYTHONPATH}:../pypy:. ../pypy/pypy/bin/rpython targetpie.py