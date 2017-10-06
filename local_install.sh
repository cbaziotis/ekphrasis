#!/bin/bash

rm -rf  build
rm -rf  ekphrasis.egg-info
rm -rf  dist

python setup.py sdist bdist_wheel

pip install --no-index --find-links=dist\ ekphrasis --force-reinstall --no-deps -U