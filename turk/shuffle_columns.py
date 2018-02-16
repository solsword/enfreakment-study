#!/usr/bin/env python3
"""
shuffle_columns.py

Shuffles comma-separated columns in a stream. Performs the same shuffle every
time.
"""

SEP = ','

import sys
import random

def main():
  fin = sys.stdin
  fout = sys.stdout
  random.seed(2**30 + 48934979)
  while True:
    try:
      line = fin.readline()
    except:
      break
    if not line:
      break
    line = line[:-1] # remove newline
    fields = line.split(SEP)
    random.shuffle(fields)
    fout.write(','.join(fields) + '\n')

if __name__ == "__main__":
  main()
