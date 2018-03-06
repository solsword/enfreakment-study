#!/bin/sh
if [ $# -ne 2 ]
then
  echo "Missing required urls filename and/or destination prefix argument(s)."
fi
for line in `cat $1`
do
  ch=`echo "$line" | cut -d, -f1`
  url=`echo "$line" | cut -d, -f2`
  wget -O $2_$ch.png $url
done
