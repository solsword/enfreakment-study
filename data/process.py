#!/usr/bin/env python3

import csv
import sys

import properties

idfields = [
  "Input.id1",
  "Input.id2",
  "Input.id3",
  "Input.id4",
  "Input.id5",
]

normalize_case = [
  "suitable",
  "lang_primary",
  "lang_secondary",
  "lang_tertiary",
  "gender_description",
  "ethnicity_description",
  "nationality_description",
]

def process(source):
  reader = csv.DictReader(source)

  results = []
  results.append( # the header
    ["participant", "id"]
  + ["character_" + ch for ch in properties.character_properties]
  + properties.participant_properties
  + properties.ratings
  + properties.personal_ratings
  )
  rout = []
  results.append(rout)

  participant = 0 # track participant ID

  for rin in reader:
    participant += 1
    for idf in idfields:
      n = idf[-1]
      cid = rin[idf]
      rout.append(participant)
      rout.append(cid)

      for ch in properties.character_properties:
        val = rin["Input.{}{}".format(ch,n)]
        rout.append(val)

      for p in properties.participant_properties:
        val = rin["Answer.{}".format(p)]
        if val in ("{}", ""):
          val = None
        elif p in normalize_case:
          val = val.title()

        rout.append(val)

      for c in properties.ratings + properties.personal_ratings:
        val = rin["Answer.{}_{}".format(c, n)]

        if val in ("{}", ""):
          val = None
        else:
          try:
            val = int(val)
          except:
            print("Nonintable: {}='{}'".format(c, val), file=sys.stderr)

        rout.append(val)

      rout = []
      results.append(rout)

  return results

def output(results, dest=sys.stdout):
  for row in results:
    pure = [str(x) if x != None else "" for x in row]
    print('\t'.join(pure), end='\n', file=dest)

if __name__ == "__main__":
  d = process(sys.stdin)
  output(d, sys.stdout)
