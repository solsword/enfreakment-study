#!/usr/bin/env python3

import sys
import json

import properties

import numpy as np

from scipy.stats import ttest_ind

from krippendorff import alpha as kr_alpha

sep_chars = ".:"

ALIASES = properties.reverse_aliases()

def get(row, index):
  """
  Retrieve from  a row according to a string index.
  """
  if (index in ALIASES):
    index = ALIASES[index]
  first = ""
  i = 0
  leftovers = False
  for i, c in enumerate(index):
    if i == 0:
      continue
    if c in sep_chars:
      leftovers = True
      break
    first += c

  if leftovers:
    rest = index[i:]
  else:
    rest = ""

  try:
    first = int(first)
  except:
    pass

  if rest:
    return get(row[first], rest)
  else:
    return row[first]

characters = [ "ryu", "chun_li", "nash", "m_bison", "cammy", "birdie", "ken", "necalli", "vega", "r_mika", "rashid", "karin", "zangief", "laura", "dhalsim", "f_a_n_g", "alex", "guile", "ibuki", "balrog", "juri", "urien", "akuma", "kolin", "ed", "abigail", "menat", "zeku", "akumat7", "alisa", "asuka", "bob", "bryan", "claudio", "dragunov", "eddy", "feng", "heihachi", "hwoarang", "jack7", "jin", "josie", "katarina", "kazumi", "kazuya", "king", "lars", "law", "lee", "leo", "lili", "luckychloe", "miguel", "nina", "paul", "raven", "shaheen", "steve", "xiaoyu", "deviljin", ]

charmap = {
  char: i
    for i, char in enumerate(characters)
}

test_agreement = [
  ".ratings.attire_ethnicity",
  ".ratings.attire_not_sexualized",
  ".ratings.attire_sexualized",
  ".ratings.attractive",
  ".ratings.chubby",
  ".ratings.costume",
  ".ratings.ethnic_stereotypes",
  ".ratings.exaggerated_body",
  ".ratings.gender_stereotypes",
  ".ratings.muscular",
  ".ratings.non_muscular",
  ".ratings.not_role_model",
  ".ratings.not_sexualized",
  ".ratings.obv_ethnicity",
  ".ratings.old",
  ".ratings.pos_ethnic_rep",
  ".ratings.pos_gender_rep",
  ".ratings.realistic_body",
  ".ratings.realistic_clothing",
  ".ratings.role_model",
  ".ratings.sexualized",
  ".ratings.skinny",
  ".ratings.ugly",
  ".ratings.young",
]

hypotheses = [
  (),
]

def main(fin):
  """
  Analyze the data from stdin.
  """
  data = json.loads(fin.read())
  records = data["records"]
  fields = data["fields"]
  rows = []
  n_raters = len(records)//5
  n_characters = len(records)//7
  for r in records:
    row = { fields[i]: r[i] for i in range(len(fields)) }
    rows.append(row)

  print("Rating agreement:")
  for t in test_agreement:
    ratings = np.full((n_raters, n_characters), np.nan)
    for row in rows:
      pid = int(get(row, ".participant.id")) - 1
      ch = get(row, ".character.id")
      cid = charmap[ch]
      if not np.isnan(ratings[pid, cid]):
        print(
          "Double-fill: [{}, {}] was {} ? {}!".format(
            pid,
            ch,
            ratings[pid, cid],
            np.isnan(ratings[pid, cid])
          ),
          file=sys.stderr
        )
        print(row, file=sys.stderr)
      ratings[pid,cid] = get(row, t)
    # DEBUG:
    """
    if "chubby" in t:
      rgrouped = {i: [] for i in range(len(characters))}
      for pid in range(ratings.shape[0]):
        for cid in range(ratings.shape[1]):
          if not np.isnan(ratings[pid,cid]):
            rgrouped[cid].append(ratings[pid,cid])
      for i, ch in enumerate(characters):
        print("{}: {}".format(ch, rgrouped[i]))
    """
    α = kr_alpha(
      reliability_data = ratings,
      value_domain = list(range(7)),
      level_of_measurement = "ordinal"
    )
    print("  {}: {}".format(t, α))

if __name__ == "__main__":
  main(sys.stdin)
