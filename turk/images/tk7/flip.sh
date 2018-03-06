#!/bin/sh
for ch in `cat flipped.csv`
do
  mogrify -flop "clean/tk7_pr_$ch.png"
done
