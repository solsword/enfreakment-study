#!/bin/sh
IFS=$'\n'
mkdir -p clean
for f in `ls TEKKEN™7/*_cs_*.jpg`
do
  #echo convert "$f" -crop 960x1080+0+0 clean/`basename "$f"`
  convert "$f" \
    -crop 960x1080+0+0 \
    -fill "#28384f" -stroke "#28384f" -draw "rectangle 310,70 416,97" \
    -fill "#070a0f" -stroke "#070a0f" -draw "rectangle 125,190 190,250" \
    -resize 1024x1024 \
    clean/`basename "$f"`
done
