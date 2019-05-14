#!/usr/bin/env bash

dir=`pwd`
rootdir="$(dirname "$dir")"

venvdir="$rootdir/venv"
echo $venvdir
if [[ ! -e $venvdir ]]; then
    echo "creating Python 3 virtual environment.."
    python3 -m venv $venvdir
    echo "Python 3 virtual environment created"
fi
source ../venv/bin/activate
pip install -r requirements.txt

