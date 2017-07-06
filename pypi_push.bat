RMDIR /S /Q build
RMDIR /S /Q ekphrasis.egg-info
RMDIR /S /Q dist

:: http://peterdowns.com/posts/first-time-with-pypi.html
python setup.py sdist bdist_wheel

:: 1 - register
:: twine register dist/*.tar.gz
for /r %%f in (dist\*.tar.gz) do echo twine register %%f
:: 2 - upload
:: twine upload dist/*
:: for /r %%f in (dist\*) do echo twine upload %%f
python setup.py sdist upload -r pypi
