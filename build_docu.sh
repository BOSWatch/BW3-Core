#!/bin/bash

echo "clean api documentation"
rm -r docu/docs/api/html
echo "generate api documentation"
doxygen docu/doxygen.ini

echo "build documentation"
source ./venv/bin/activate
python3 -m mkdocs build -f docu/mkdocs.yml
deactivate