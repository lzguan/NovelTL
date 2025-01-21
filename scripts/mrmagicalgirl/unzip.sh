#!/bin/bash

for i in *.zip; do
    mkdir ${i::-4}
    unzip -d ${i::-4} $i
done