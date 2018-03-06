#!/bin/sh
for line in `cat urls`
do
  ch=`echo "$line" | cut -d, -f1`
  url=`echo "$line" | cut -d, -f2`
  wget -O clean/sfv_oa_$ch.jpg $url
done
