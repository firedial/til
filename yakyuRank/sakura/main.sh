#!/bin/bash

git pull
git -C ../../../web-site-sakura pull

if [ "$#" -ne 1]; then
    exit 1
fi

python3 ./calc.py $1

git add .
git commit -m "結果反映"
git push

mv ./data.csv ../../../web-site-sakura/public/csv/data.csv

git -C ../../../web-site-sakura add .
git -C ../../../web-site-sakura commit -m "結果反映"
git -C ../../../web-site-sakura push

