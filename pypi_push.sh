#!/bin/bash

rm -rf build
rm -rf ekphrasis.egg-info
rm -rf dist

python setup.py sdist bdist_wheel

twine register dist/*.tar.gz
twine upload dist/*
python setup.py sdist upload -r pypi
