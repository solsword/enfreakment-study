#!/usr/bin/env python3

import csv
import sys

import json

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

def nv(x):
  if x == "":
    return None
  else:
    f = float(x)
    if f == int(f):
      return int(f)
    else:
      return f

def process(source):
  reader = csv.DictReader(source, dialect="excel-tab")

  rows = [rin for rin in reader]

  aliases = {
    ".ratings:{}".format(i): ratings[i]
    for i in range(len(ratings))
  }
  for i in range(len(ratings)):
    aliases[".avg_ratings:{}".format(i)] = "avg_" + ratings[i]

  result = {
    "aliases": aliases,
    "records": [],
    "fields": (
      ["participant", "id"]
    + ["character_" + ch for ch in character_properties]
    + participant_properties
    + ["ratings", "avg_ratings"]
    ),
  }

  ungrouped = 2 + len(character_properties) + len(participant_properties)

  for row in rows:
    rvs = list(row.values())
    nr = rvs[:ungrouped] + [
      [nv(x) for x in rvs[ungrouped:ungrouped + len(ratings)]],
      [nv(x) for x in rvs[ungrouped + len(ratings):]],
    ]
    result["records"].append(nr)

  return result

def output(result, dest=sys.stdout):
  dest.write(json.dumps(result))

if __name__ == "__main__":
  d = process(sys.stdin)
  output(d, sys.stdout)
