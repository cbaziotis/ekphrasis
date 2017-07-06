RMDIR /S /Q build
RMDIR /S /Q keras_utilities.egg-info
RMDIR /S /Q dist

python setup.py sdist bdist_wheel

pip install --no-index --find-links=dist\ ekphrasis --force-reinstall --no-deps -U