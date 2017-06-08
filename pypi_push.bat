RMDIR /S /Q build
RMDIR /S /Q ekphrasis.egg-info
RMDIR /S /Q dist

python setup.py sdist bdist_wheel
twine upload dist/*