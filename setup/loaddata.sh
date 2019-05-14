#!/usr/bin/env bash

dir=`pwd`
rootdir="$(dirname "$dir")"

# Download IMDB files
wget 'https://datasets.imdbws.com/name.basics.tsv.gz'
gunzip name.basics.tsv.gz

wget 'https://datasets.imdbws.com/title.basics.tsv.gz'
gunzip title.basics.tsv.gz

# Generate fixtures
mkdir -p $rootdir/apis/fixtures
python generate_fixtures.py --imdbfilesdir=$dir --fixturedir=$rootdir/apis/fixtures --limit=5000

rm name.basics.tsv title.basics.tsv.gz

# Setup db and load data
python manage.py makemigrations apis
python manage.py migrate
python manage.py loaddata apis/fixtures/movies.json

