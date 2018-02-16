#!/usr/bin/env python3
"""
Reads all_chars.csv and divides the characters into groups, which it prints as
CSV lines containing character indices.
"""

import csv
import sys
import collections

import numpy as np

# How many items per group
GROUP_SIZE = 5

# How many pairs are present in each group
PAIRS_PER_GROUP = (GROUP_SIZE * (GROUP_SIZE - 1)) // 2

# How many times each item should appear
EVAL_COUNT = 7

# Which columns should be diverse (have at least 2 values) within each group
ENSURE_DIVERSITY = [
  "gender",
  "origin"
]

def read_characters(filename):
  with open(filename) as fin:
    raw = fin.readlines()

  rows = []
  keys = raw[0][:-1].split(',')
  for raw_row in raw[1:]:
    bits = []
    while raw_row:
      if raw_row[0] == '"':
        eq = raw_row[1:].index('"')
        bits.append(raw_row[1:eq+1])
        raw_row = raw_row[eq+3:]
      else:
        if ',' in raw_row:
          ni = raw_row.index(',')
          bits.append(raw_row[:ni])
          raw_row = raw_row[ni+1:]
        else:
          bits.append(raw_row[:-1])
          raw_row = ''

    if len(bits) != len(keys):
      print(
        "Error: wrong number of bits ({} != {}):\n{}".format(
          len(bits),
          len(keys),
          ','.join(bits)
        )
      )
    rows.append({})
    for i in range(len(keys)):
      rows[-1][keys[i]] = bits[i]

  return rows

def group_size(rows):
  n_groups = (len(rows) * EVAL_COUNT) / GROUP_SIZE
  if n_groups != int(n_groups):
    print("Error: group size doesn't work out to an integer!", file=sys.stderr)
    return None
  else:
    return int(n_groups)


def random_configuration(chars):
  """
  Generates a completely random grouping of characters.
  """
  n_groups = group_size(chars)
  groups = np.array([
    np.random.choice(range(len(chars)), size=GROUP_SIZE, replace=False)
      for i in range(n_groups)
  ])
  return groups

def diversity(chars, grouping, prop):
  """
  Computes the diversity score of a grouping for a given property.
  Each row that is diverse gets a 1, each that isn't gets a 0.
  """
  score = 0
  for row in grouping:
    first = chars[row[0]][prop]
    for i in range(1,len(row)):
      if chars[row[i]][prop] != first:
        score += 1
        break
      # otherwise keep iterating

  return score

def homogeneous_rows(chars, grouping, prop):
  """
  Same computation as diversity score, but returns a mapping from homogeneous
  row indices to their property values.
  """
  homogeneous = {}
  for idx, row in enumerate(grouping):
    first = chars[row[0]][prop]
    diverse = False
    for i in range(1,len(row)):
      if chars[row[i]][prop] != first:
        diverse = True
        break
      # otherwise keep iterating
    if not diverse:
      homogeneous[idx] = first

  return homogeneous

def pairs_score(chars, grouping):
  """
  Computes the number times each possible pairing occurs in the given grouping,
  and returns a score based on that.
  """
  nc = len(chars)
  total_pairs = PAIRS_PER_GROUP * len(grouping)
  possible_pairs = (nc * (nc - 1)) # times two to include both orderings of each
  target_pair_occurances = total_pairs / possible_pairs
  itpo = int(target_pair_occurances)
  if itpo == target_pair_occurances:
    valid_pair_frequencies = [ itpo ]
  else:
    valid_pair_frequencies = [ itpo, itpo + 1 ]

  print("total pairs:", total_pairs)
  print("possible pairs:", possible_pairs)

  pairs = collections.defaultdict(lambda: 0)
  for row in grouping:
    for i in range(len(row)):
      for j in range(i+1, len(row)):
        k = (row[i], row[j])
        pairs[k] += 1

  score = 0
  for i in range(nc):
    for j in range(i+1, nc):
      k1 = (i, j)
      k2 = (j, i)
      if pairs[k1] in valid_pair_frequencies:
        score += 1
      if pairs[k2] in valid_pair_frequencies:
        score += 1

  return score

def pairs_to_break(chars, grouping):
  """
  Works like pairs_score, but instead of just computing a score, it returns an
  array the same size as the given grouping specifying which group
  members could be changed to (potentially) improve the pair score of the given
  grouping, along with mappings from initial and final pair members to matching
  members that would help increase the pairs_score.

  The change map entries are the index of another item in the same group (row)
  which is creating a superfluous pair; if the index points to itself that item
  isn't involved in a superfluous pair. Note that one end of a pair might chain
  to another entry, and not all pairs might be identified if they overlap too
  much.
  """
  nc = len(chars)
  total_pairs = PAIRS_PER_GROUP * len(grouping)
  possible_pairs = (nc * (nc - 1)) # times two to include both orderings of each
  target_pair_occurances = total_pairs / possible_pairs
  itpo = int(target_pair_occurances)
  if itpo == target_pair_occurances:
    min_pair_frequency = itpo
    max_pair_frequency = itpo
  else:
    min_pair_frequency = itpo
    max_pair_frequency = itpo + 1

  # Pair-index array defaulting to self-pairs:
  change_points = np.zeros_like(grouping)
  for i in range(len(change_points)):
    for j in range(len(change_points[i])):
      change_points[i][j] = j

  pairs = collections.defaultdict(lambda: 0)
  for idx, row in enumerate(grouping):
    for i in range(len(row)):
      for j in range(i+1, len(row)):
        k = (row[i], row[j])
        pairs[k] += 1
        if pairs[k] > max_pair_frequency: # this grouping cost points
          change_points[idx,i] = 1
          change_points[idx,j] = 1

  # Pair-value mappings:
  initial_map = collections.defaultdict(lambda: [])
  final_map = collections.defaultdict(lambda: [])

  for i in range(nc):
    for j in range(i+1, nc):
      k1 = (i, j)
      k2 = (j, i)
      if pairs[k1] < min_pair_frequency:
        initial_map[i].append(j)
        final_map[j].append(i)
      if pairs[k2] < min_pair_frequency:
        initial_map[j].append(i)
        final_map[i].append(j)

  return (change_points, initial_map, final_map)

def better_groupings(chars, grouping):
  """
  Computes a list of groupings better then the given grouping, that are just a
  single change away.
  """
  results = []
  # All the ways we could increase diversity:
  for prp in ENSURE_DIVERSITY:
    hrows = homogeneous_rows(chars, grouping, prp)
    if hrows:
      for row in hrows:
        val = hrows[row] # value to avoid to increase diversity
        for i in range(len(chars)):
          if chars[i][prp] != val: # items that would add diversity
            for j in range(len(grouping[row])): # each possible replacement idx
              fresh = np.copy(grouping)
              fresh[row][j] = i
              results.append(fresh)

  # All the ways we could improve pair counts:
  change_points, initial_map, final_map = pairs_to_break(chars, grouping)
  for i in range(len(change_points)):
    for j in range(len(change_points[i])):
      oi = change_points[i][j]
      if oi != j:
        if oi > j:
          hungry = initial_map[grouping[i][oi]]
          if hungry:
            for ov in hungry:
              fresh = np.copy(grouping)
              fresh[i][oi] = ov
              results.append(fresh)
        else:
          hungry = final_map[grouping[i][oi]]
          if hungry:
            for ov in hungry:
              fresh = np.copy(grouping)
              fresh[i][oi] = ov
              results.append(fresh)

  return results

def main():
  """
  Reads all_chars.csv and prints out generated groups.
  """
  np.random.seed(182081029)

  chars = read_characters("all_chars.csv")

  rc = random_configuration(chars)

  print(homogeneous_rows(chars, rc, "gender"))
  print(pairs_to_break(chars, rc))

  print(diversity(chars, rc, "gender"))
  print(diversity(chars, rc, "origin"))
  print(pairs_score(chars, rc))

  print('-'*80)
  #print(better_groupings(chars, rc))


if __name__ == "__main__":
  main()
