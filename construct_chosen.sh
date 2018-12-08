#!/usr/bin/env bash

mkdir -p chosen
rm -r chosen/*

while read p; do
    cp configs/${p}.json chosen/
    python sinusvase.py chosen/${p}.json
    mv vase.stl chosen/${p}.stl
done < $1
