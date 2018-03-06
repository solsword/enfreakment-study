#!/bin/sh
IFS=$'\n'
for f in `ls January13_2018/*.jpg`
do
  #echo "convert \"$f\" -crop 960x1080+0+0 clean/sfv_`basename \"$f\" | cut -d. -f1`".png
  convert "$f" -crop 960x1080+0+0 clean/`basename "$f"`
done
