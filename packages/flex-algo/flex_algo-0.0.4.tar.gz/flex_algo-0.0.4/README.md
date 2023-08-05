# This package includes the most common used data structures and algorithms in python

## Install the package
```commandline
pip install flex-algo
```

## Publish to PyPI
```commandline
pip install --upgrade build
pip install --upgrade twine

python -m build
python -m twine upload dist/*
```

## Test the package
```commandline
pip install -e .
pytest tests/*
```
