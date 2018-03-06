#!/bin/sh
IFS=$'\n'
for f in `ls head_images/*.png`
do
  cp "$f" clean/`basename "$f"`
done
