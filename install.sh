#!/bin/bash
echo "Building ASCEND framework..."
python setup.py sdist
echo "Installing ASCEND framework..."
python -m pip install .