#!/bin/bash
echo "Building ASCEND Controller framework..."
python setup.py sdist
echo "Installing ASCEND Controller framework..."
pip install .