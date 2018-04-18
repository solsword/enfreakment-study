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

constructs = [
  ["attractiveness", [("+", "attractive"), ("-", "ugly")]],
  ["youth", [("+", "young"), ("-", "old")]],
  ["sexualization", [("+", "sexualized"), ("-", "not_sexualized")]],
  ["muscles", [("+", "muscular"), ("-", "non_muscular")]],
  ["thinness", [("+", "skinny"), ("-", "chubby")]],
  ["body_realism", [("+", "realistic_body"), ("-", "exaggerated_body")]],
  ["clothing_realism", [("+", "realistic_clothing"), ("-", "costume")]],
  ["combined_realism",
   [("+", "realistic_body"), ("-", "exaggerated_body"), ("+", "realistic_clothing"), ("-", "costume")]],
  ["attire_sexualization",
   [("+", "attire_sexualized"), ("-", "attire_not_sexualized")]],
  ["combined_sexualization",
   [("+", "sexualized"), ("-", "not_sexualized"), ("+", "attire_sexualized"), ("-", "attire_not_sexualized")]],
  ["combined_ethnic_signals",
   [("+", "obv_ethnicity"), ("+", "attire_ethnicity")]],
  ["positive_gender_rep", [("+", "pos_gender_rep"), ("-", "gender_stereotypes")]],
  ["positive_ethnic_rep", [("+", "pos_ethnic_rep"), ("-", "ethnic_stereotypes")]],
  ["admirability", [("+", "role_model"), ("-", "not_role_model")]],
  ["combined_admirability", [("+", "role_model"), ("-", "not_role_model"), ("+", "pos_gender_rep"), ("-", "gender_stereotypes"), ("+", "pos_ethnic_rep"), ("-", "ethnic_stereotypes")]],
]

skin_tones = {
  "abigail": "fair",
  "akuma": "dark",
  "alex": "fair",
  "balrog": "dark",
  "birdie": "dark",
  "cammy": "fair",
  "chun_li": "fair",
  "dhalsim": "dark",
  "ed": "fair",
  "f_a_n_g": "fair",
  "guile": "fair",
  "ibuki": "fair",
  "juri": "fair",
  "karin": "fair",
  "ken": "fair",
  "kolin": "fair",
  "laura": "dark",
  "m_bison": "fair",
  "menat": "dark",
  "nash": "fair",
  "necalli": "dark",
  "rashid": "fair",
  "r_mika": "fair",
  "ryu": "fair",
  "sakura": "fair",
  "urien": "dark",
  "vega": "fair",
  "zangief": "fair",
  "zeku": "fair",
  "zeku": "fair",
  "akumat7": "dark",
  "alisa": "fair",
  "asuka": "fair",
  "bob": "fair",
  "bryan": "fair",
  "claudio": "fair",
  "deviljin": "fair",
  "dragunov": "fair",
  "eddy": "dark",
  "eliza": "fair",
  "feng": "fair",
  "gigas": "N/A",
  "heihachi": "fair",
  "hwoarang": "fair",
  "jack7": "fair",
  "jin": "fair",
  "josie": "fair",
  "katarina": "fair",
  "kazumi": "fair",
  "kazuya": "fair",
  "king": "fair",
  "lars": "fair",
  "law": "fair",
  "lee": "fair",
  "leo": "fair",
  "lili": "fair",
  "luckychloe": "fair",
  "miguel": "dark",
  "nina": "fair",
  "paul": "fair",
  "raven": "dark",
  "shaheen": "fair",
  "steve": "fair",
  "xiaoyu": "fair",
  "yoshimitsu": "N/A",
}

def agreement(row, measure):
  val = nv(row[measure])
  if val == None:
    return 0
  else:
    return max(0, val - 4)

def disagreement(row, measure):
  val = nv(row[measure])
  if val == None:
    return 0
  else:
    return max(0, 4 - val)

def full_agreement(row, measure):
  val = nv(row[measure])
  if val == None:
    return 0
  else:
    return val - 4

def supermodel_enfreakment(row):
  return (
  - full_agreement(row, "avg_attire_not_sexualized")
  + full_agreement(row, "avg_attire_sexualized")
  + full_agreement(row, "avg_attractive")
  - agreement(row, "avg_ugly")
  - agreement(row, "avg_chubby")
  + full_agreement(row, "avg_skinny")
  + agreement(row, "avg_exaggerated_body")
  - full_agreement(row, "avg_not_sexualized")
  + full_agreement(row, "avg_sexualized")
  - agreement(row, "avg_old")
  + agreement(row, "avg_young")
  + disagreement(row, "avg_realistic_body")
  )

def brute_enfreakment(row):
  return (
    full_agreement(row, "avg_muscular")
  - full_agreement(row, "avg_non_muscular")
  + full_agreement(row, "avg_ugly")
  - full_agreement(row, "avg_attractive")
  + agreement(row, "avg_exaggerated_body")
  + agreement(row, "avg_chubby")
  - agreement(row, "avg_attire_sexualized")
  - agreement(row, "avg_sexualized")
  - agreement(row, "avg_skinny")
  )

def ethnic_enfreakment(row):
  return (
    full_agreement(row, "avg_attire_ethnicity")
  + full_agreement(row, "avg_ethnic_stereotypes")
  + full_agreement(row, "avg_obv_ethnicity")
  )

def unmartial_enfreakment(row):
  return (
    full_agreement(row, "avg_exaggerated_body")
  - full_agreement(row, "avg_realistic_body")
  + full_agreement(row, "avg_non_muscular")
  - full_agreement(row, "avg_muscular")
  + agreement(row, "avg_chubby")
  + agreement(row, "avg_skinny")
  + agreement(row, "avg_old")
  )

def villain_enfreakment(row):
  return (
    full_agreement(row, "avg_not_role_model")
  - full_agreement(row, "avg_role_model")
  - full_agreement(row, "avg_pos_ethnic_rep")
  - full_agreement(row, "avg_pos_gender_rep")
  )

enfreakments = {
  "supermodel": supermodel_enfreakment,
  "brute": brute_enfreakment,
  "ethnic": ethnic_enfreakment,
  "unmartial": unmartial_enfreakment,
  "villain": villain_enfreakment,
}

enfreakment_types = [
  "supermodel",
  "brute",
  "ethnic",
  "unmartial",
  "villain",
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

  for (i, (name, components)) in enumerate(constructs):
    aliases[".constructs:{}".format(i)] = name
    aliases[".avg_constructs:{}".format(i)] = "avg_" + name

  for i, t in enumerate(enfreakment_types):
    aliases[".enfreakments:{}".format(i)] = t

  result = {
    "aliases": aliases,
    "records": [],
    "fields": (
      [
        "participant",
        "id",
        "country_count",
        "character_token",
        "character_japanese",
        "character_skin_tone",
      ]
    + ["character_" + ch for ch in character_properties]
    + participant_properties
    + ["ratings", "avg_ratings", "constructs", "avg_constructs", "enfreakments"]
    ),
  }

  ungrouped = 2 + len(character_properties) + len(participant_properties)

  for row in rows:
    rvs = list(row.values())
    raw_ratings = rvs[ungrouped:ungrouped + len(ratings)]
    avg_ratings = rvs[ungrouped + len(ratings):]

    efk = [enfreakments[t](row) for t in enfreakment_types]

    if row["character_country"] == "Unknown":
      c_count = 1
    else:
      c_count = sum(
        1 for r in rows if r["character_country"] == row["character_country"]
      ) // 7

    cons = []
    avg_cons = []
    for (name, components) in constructs:
      cval = 0
      aval = 0
      cdenom = 0
      adenom = 0
      for sign, field in components:
        val = nv(row[field])
        # Add to average constructs
        adenom += 1
        if sign == "+":
          aval += nv(row["avg_" + field])
        else:
          aval += 8 - nv(row["avg_" + field])
        if val != None:
          # Value present: add to individual constructs as well
          cdenom += 1
          if sign == "+":
            cval += val
          else:
            cval += 8 - val
      cval /= cdenom
      aval /= adenom
      cons.append(cval)
      avg_cons.append(aval)

    nr = (
      rvs[:2]
    + [
        c_count,
        ["Token", "Minority", "Majority"][(c_count > 2) + (c_count > 5)],
        ["Other", "Japanese"][row["character_country"] == "Japan"],
        skin_tones[row["id"]]
      ]
    + rvs[2:ungrouped]
    + [
        [nv(x) for x in raw_ratings],
        [nv(x) for x in avg_ratings],
        cons,
        avg_cons,
        efk
      ]
    )

    result["records"].append(nr)

  return result

def output(result, dest=sys.stdout):
  dest.write(json.dumps(result))

if __name__ == "__main__":
  d = process(sys.stdin)
  output(d, sys.stdout)
