#!/bin/bash

for i in *.zip; do
    mv "$i" "./chapter${i: -11}"
done