#!/bin/bash
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
cd ${0%/*} || exit 1    # Run from this directory

function read_dir() {
	for file in `ls $1`
	do
		if [ -d $1"/"$file ]; # 判断是否是目录，是目录则递归
		then
			read_dir $1"/"$file
		elif [ -f $1"/"$file ]; # 判断是否是文件，输出屏幕
		then
			echo  $1"/"$file
		else
			echo #$1"/"$file
		fi
	done
}
for file in $(read_dir .)
do
    if [ "${file##*.}"x = "flac"x ];then
        noSuffixfile=${file%\.*}
        ffmpeg  -i $file  -q:a 0 "$noSuffixfile.mp3"
    fi
done

IFS=$SAVEIFS
