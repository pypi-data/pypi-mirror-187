# gb_module

## Build

```
# build it
python3 setup.py sdist bdist_wheel
# install it locally
pip3 install -e .
# upload to pypi (don't forget to increase the version number)
python3 -m twine upload dist/*
```
