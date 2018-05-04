#!/usr/bin/env python3

import csv
import sys

import json

import properties

def process(source):
  reader = csv.DictReader(source, dialect="excel-tab")

  rows = [rin for rin in reader]

  aliases = properties.construct_aliases()

  columns = (
    [
      "participant",
      "character",
      "ratings",
      "personal_ratings",
      "med_ratings",
      "med_personal",
      "participant_personal",
      "constructs",
      "med_constructs",
      "enfreakments",
    ]
  )

  result = {
    "aliases": aliases,
    "records": [],
    "fields": columns,
  }

  for row in rows:
    fields = {}

    fields["participant"] = { "id": row["participant"] }
    for pp in properties.participant_properties:
      if pp == "normalized_ethnicity":
        fields["participant"][pp] = { c: 1 for c in row[pp].split(' + ') }
      else:
        fields["participant"][pp] = row[pp]

    fields["character"] = { "id": row["id"] }
    for cp in properties.character_properties:
      key = "character_" + cp
      fields["character"][cp] = row[key]

    fields["ratings"] = [properties.nv(row[rt]) for rt in properties.ratings]
    fields["personal_ratings"] = [
      properties.nv(row[rt])
        for rt in properties.personal_ratings
    ]
    fields["med_ratings"] = [
      properties.nv(row["med_" + rt])
        for rt in properties.ratings
    ]
    fields["med_personal"] = [
      properties.nv(row["med_" + rt])
        for rt in properties.personal_ratings
    ]
    fields["participant_personal"] = [
      properties.nv(row["participant_" + rt])
        for rt in properties.personal_ratings
    ]

    fields["enfreakments"] = [
      properties.enfreakments[t](row)
        for t in properties.enfreakment_types
    ]

    if row["character_country"] == "Unknown":
      c_count = 1
    else:
      c_count = sum(
        1 for r in rows if r["character_country"] == row["character_country"]
      ) // 7

    fields["character"]["country_count"] = c_count

    fields["character"]["is_token"] = [
      "Token",
      "Minority",
      "Majority"
    ][(c_count > 2) + (c_count > 5)]

    fields["character"]["is_japanese"] = [
      "Other",
      "Japanese"
    ][row["character_country"] == "Japan"]

    fields["character"]["skin_tone"] = properties.skin_tones[row["id"]]

    fields["constructs"] = [
      properties.nv(row["@" + cns])
        for (cns, _) in properties.constructs
    ]
    fields["med_constructs"] = [
      properties.nv(row["med_@" + cns])
        for (cns, _) in properties.constructs
    ]

    nr = [ fields[k] for k in columns ]

    result["records"].append(nr)

  return result

def output(result, dest=sys.stdout):
  dest.write(json.dumps(result))

if __name__ == "__main__":
  d = process(sys.stdin)
  output(d, sys.stdout)
