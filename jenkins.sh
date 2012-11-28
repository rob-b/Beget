#!/bin/sh

if [ -d ".env" ]; then
 echo "**> virtualenv exists"
else
 echo "**> creating virtualenv"
 virtualenv .env
 mkdir -p $HOME/pip-cache
 .env/bin/pip install --download-cache $HOME/pip-cache nose==1.1.2 coverage pylint
fi

. .env/bin/activate
PYTHONPATH=. python setup.py nosetests --with-xunit --with-coverage --cover-package=beget --cover-inclusive beget/tests.py
coverage xml
pylint -f parseable -d I0011,R0801 beget | tee pylint.out

