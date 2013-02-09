#!/bin/bash

# Simple pie compiler
# It supposes that PYPY is situated in the directory '../pypy'
# sery0ga

PYTHONPATH=${PYTHONPATH}:../pypy:. ../pypy/rpython/bin/rpython targetpie.py