#!/usr/bin/env python3
"""
multiethnic.py

Processes ethnicities list to determine distribution of multiple ethnicities.
"""

import sys

multi = 0
single = 0
ignore = [ "American", "European" ]

for line in sys.stdin.readlines():
  bits = line.split()
  first = bits[0]
  if first == '':
    count = int(bits[1])
    rest = bits[2:]
  else:
    count = int(bits[0])
    rest = bits[1:]
  count /= 5 # 5 records per participant
  count = round(count)
  parts = ' '.join(rest).split(' + ')
  for ign in ignore:
    try:
      parts.remove(ign)
    except:
      pass
  if len(parts) <= 1:
    single += count
  else:
    multi += count

print("Single ethnicity: {}\nMultiple ethnicity: {}".format(single, multi))
