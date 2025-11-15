#!/bin/sh

if [ -d ./dist ] ; then
  rm -fr dist
fi
python -m build
python -m twine upload  dist/*