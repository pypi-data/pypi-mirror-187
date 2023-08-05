# tweet-py
Python package which to access the Tweet data without API


python  -m venv venv
source venv/bin/activate
pip install wheel setuptools twine
python setup.py sdist bdist_wheel
python -m twine upload dist/*
