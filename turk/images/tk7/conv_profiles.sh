#!/bin/sh
IFS=$'\n'
for f in `ls body_images/*.png`
do
  #echo convert "$f" -crop 2880x2880+0+0 -resize 1024x1024 clean/`basename "$f"`
  convert "$f" -crop 2032x2032+848+0 -resize 1024x1024 clean/`basename "$f"`
done
