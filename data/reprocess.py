#!/usr/bin/env python3

import csv
import sys

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
  reader = csv.DictReader(source, dialect="excel-tab")

  rows = [rin for rin in reader]

  characters = sorted(list(set(row["id"] for row in rows)))

  forchar = {
    ch: [rin for rin in rows if rin["id"] == ch]
      for ch in characters
  }

  averages = {}

  for ch in forchar:
    averages[ch] = []
    for rt in ratings:
      pure = [ int(row[rt]) for row in forchar[ch] if row[rt] != "" ]
      averages[ch].append(sum(pure) / len(pure))

  result = []
  result.append(
    ["participant", "id"]
  + ["character_" + ch for ch in character_properties]
  + participant_properties
  + ratings
  + ["avg_" + rt for rt in ratings]
  )
  for row in rows:
    nr = list(row.values()) + averages[row["id"]]
    result.append(nr)

  return result

def output(results, dest=sys.stdout):
  for row in results:
    pure = [str(x) if x != None else "" for x in row]
    print('\t'.join(pure), end='\n', file=dest)

if __name__ == "__main__":
  d = process(sys.stdin)
  output(d, sys.stdout)
