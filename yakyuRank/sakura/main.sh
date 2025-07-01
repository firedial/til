#!/bin/bash

echo "---------- cd ----------"
cd ~/prog/sakura-yakyuu/til/yakyuRank/sakura

echo "---------- git pull ----------"
git pull
git -C ../../../web-site-sakura pull

if [ $# -ne 1 ] ; then
    echo "---------- no arg ----------"
    exit 1
fi

echo "---------- exec ----------"
python3 ./calc.py $1

if [ $? -ne 0 ] ; then
    echo "---------- exec error ----------"
    exit 1
fi

echo "---------- git push til ----------"
git add .
git commit -m "結果反映"
git push

echo "---------- mv ----------"
mv ./data.csv ../../../web-site-sakura/public/csv/data.csv

echo "---------- git push sakura ----------"
git -C ../../../web-site-sakura add .
git -C ../../../web-site-sakura commit -m "結果反映"
git -C ../../../web-site-sakura push
