#!/bin/sh
IFS=$'\n'
for f in `ls TEKKEN™7/*_ig_*.jpg`
do
  #echo convert "$f" -crop 960x1080+0+0 clean/`basename "$f"`
  convert "$f" -crop 960x1080+0+0 -resize 1024x1024 clean/`basename "$f"`
done
