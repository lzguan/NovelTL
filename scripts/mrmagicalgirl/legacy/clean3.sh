#!/bin/bash

for fol in $(ls -d */); do
    echo Making folder ${fol}img
    if [ -z "$(find $fol -type f -name '*.jpg')" ] && [ -z $(find $fol -type f -name '*.gif') ]; then
        echo No images found, aborted
    else
        mkdir ${fol}img
        echo Moving images to ${fol}img:
        mv -t ${fol}img ${fol}*.jpg
        mv -t ${fol}img ${fol}*.gif
    fi
done