#!/usr/bin/env python3

import csv
import sys

import numpy as np

import properties

def process(source):
  reader = csv.DictReader(source, dialect="excel-tab")

  rows = [rin for rin in reader]

  for rn, row in enumerate(rows):
    for (cns, _) in properties.constructs:
      try:
        row["@" + cns] = properties.extract_construct(row, cns)
      except:
        raise ValueError(
          "Couldn't extract construct '{}' from line {}:\n{}".format(
            cns,
            rn + 2,
            row
          )
        )

  characters = sorted(list(set(row["id"] for row in rows)))
  participants = sorted(list(set(row["participant"] for row in rows)))

  forchar = {
    ch: [rin for rin in rows if rin["id"] == ch]
      for ch in characters
  }

  forpart = {
    part: [rin for rin in rows if rin["participant"] == part]
      for part in participants
  }

  ch_medians = {}
  pt_medians = {}

  group_by_character = (
    properties.ratings
  + properties.personal_ratings
  + [ ("@" + cns) for (cns, _) in properties.constructs ]
  )

  group_by_participant = properties.personal_ratings

  for ch in forchar:
    ch_medians[ch] = []
    for rt in group_by_character:
      pure = [int(row[rt]) for row in forchar[ch] if row[rt] not in ("", None)]
      ch_medians[ch].append(np.median(pure))

  for part in forpart:
    pt_medians[part] = []
    for rt in group_by_participant:
      pure = [ int(row[rt]) for row in forpart[part] if row[rt] != "" ]
      pt_medians[part].append(np.median(pure))

  result = []
  result.append(
    ["participant", "id"]
  + ["character_" + ch for ch in properties.character_properties]
  + properties.participant_properties
  + properties.ratings
  + properties.personal_ratings
  + ["@" + cns for (cns, _) in properties.constructs]
  + ["med_" + rt for rt in group_by_character]
  + ["participant_" + rt for rt in group_by_participant]
  )
  for row in rows:
    result.append(
      list(row.values())
    + ch_medians[row["id"]]
    + pt_medians[row["participant"]]
    )

  return result

def output(results, dest=sys.stdout):
  for row in results:
    pure = [str(x) if x != None else "" for x in row]
    print('\t'.join(pure), end='\n', file=dest)

if __name__ == "__main__":
  d = process(sys.stdin)
  output(d, sys.stdout)
