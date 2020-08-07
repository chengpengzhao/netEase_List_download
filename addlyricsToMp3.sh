#!/bin/bash
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
cd ${0%/*} || exit 1    # Run from this directory

for file in `ls .`
do
    if [ "${file##*.}"x = "mp3"x ];then
        python3 downloadLyrics.py $file;
        eyeD3 --add-lyrics "$file.lrc" $file;
        rm "$file.lrc"
    fi
done

IFS=$SAVEIFS
