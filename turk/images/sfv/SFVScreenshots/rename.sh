#!/bin/sh
# loop through all files whose names start with STREET
files=`ls STREET* | sed -e "s/ /-^-^/g"`
for f in $files
do
  # Set variable to number part of filename
  nr=`echo "$f" | cut -d_ -f2 | cut -d. -f1`
  # Compute the real filename
  tf=`echo "$f" | sed -e "s/-^-^/ /g"`
  # Test whether number part of filename is smaller than value.
  if [ $nr -le 20180107192214 ]
  then
    # if so, rename to one thing
    mv "$tf" sfv-ingame-$nr.jpg
    # our old dummy test to make sure things would work properly
    #echo "mv \"$tf\" sfv-ingame-$nr.jpg"
  else
    # else rename differently
    mv "$tf" sfv-select-$nr.jpg
    # our old dummy test to make sure things would work properly
    #echo "mv \"$tf\" sfv-select-$nr.jpg"
  fi
done
