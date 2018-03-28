#!/usr/bin/env python3

import csv
import sys

idfields = [
  "Input.id1",
  "Input.id2",
  "Input.id3",
  "Input.id4",
  "Input.id5",
]

character_properties = [
  "country",
  "gendergroup",
  "bio",
  "quote",
]

participant_properties = [
  "suitable",
  "age",
  "education",
  "played_specific",
  "played_franchise",
  "played_fighting",
  "played_any",
  "play_frequency",
  "watched_franchise",
  "watched_fighting",
  "lang_primary",
  "lang_secondary",
  "lang_tertiary",
  "lang_extra",
  "gender_description",
  "ethnicity_description",
  "nationality_description",
  "feedback",
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

ratings = [
  "attire_ethnicity",
  "attire_not_sexualized",
  "attire_sexualized",
  "attractive",
  "chubby",
  "costume",
  "ethnic_familiarity",
  "ethnic_match",
  "ethnic_stereotypes",
  "exaggerated_body",
  "gender_stereotypes",
  "identification",
  "muscular",
  "non_muscular",
  "not_role_model",
  "not_sexualized",
  "obv_ethnicity",
  "old",
  "pos_ethnic_rep",
  "pos_gender_rep",
  "realistic_body",
  "realistic_clothing",
  "role_model",
  "sexualized",
  "skinny",
  "ugly",
  "young",
]

def process(source):
  reader = csv.DictReader(source)

  results = []
  results.append( # the header
    ["participant", "id"]
  + ["character_" + ch for ch in character_properties]
  + participant_properties
  + ratings
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

      for ch in character_properties:
        val = rin["Input.{}{}".format(ch,n)]
        rout.append(val)

      for p in participant_properties:
        val = rin["Answer.{}".format(p)]
        if val in ("{}", ""):
          val = None
        elif p in normalize_case:
          val = val.title()

        rout.append(val)

      for c in ratings:
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
