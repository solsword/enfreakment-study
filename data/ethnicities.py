#!/usr/bin/env python3
"""
multiethnic.py

Processes ethnicities list to determine distribution of multiple ethnicities.
"""

import sys

multi = 0
single = 0
semi_equal = {
  "White": [ "American", "European" ],
  "Hispanic": [ "Latinx" ]
}

counts = {}
multi_counts = {}

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

  ethnicity_count = len(parts)
  for key in semi_equal:
    if key in parts and any(x in parts for x in semi_equal[key]):
      ethnicity_count -= 1

  multi_ethnic = ethnicity_count > 1

  for p in parts:
    if p not in counts:
      counts[p] = 0
    if p not in multi_counts:
      multi_counts[p] = 0

    counts[p] += count

    if multi_ethnic:
      multi_counts[p] += count

  if multi_ethnic:
    multi += count
  else:
    single += count

print("Single ethnicity: {}\nMultiple ethnicity: {}".format(single, multi))
print('-'*80)
for key in sorted(counts, key=lambda k: (-counts[k], k)):
  print("{}: {} ({})".format(key, counts[key], multi_counts[key]))
