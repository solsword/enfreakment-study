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
  (".constructs.body_realism", ".character.country", "Japan", "↑"),
  (".constructs.muscles", ".character.gendergroup", "women", "↓"),
  (".constructs.thinness", ".character.country", "Japan", "↑"),
  (".constructs.thinness", ".character.gendergroup", "women", "↑"),

  (".constructs.youth", ".character.gendergroup", "women", "↑"),

  (".constructs.attractiveness", ".character.gendergroup", "women", "↑"),
  (".constructs.attractiveness", ".character.country", "Japan", "↑"),
  (".constructs.attractiveness", ".character.is_token","Majority", "↑"),
  (".constructs.attractiveness", ".character.is_token", "Token", "↓"),

  (".constructs.combined_sexualization", ".character.gendergroup", "women","↑"),

  (".constructs.clothing_realism", ".character.gendergroup", "women", "↓"),
  (".constructs.clothing_realism", ".character.country", "Japan", "↑"),
  (".constructs.clothing_realism", ".character.is_token", "Majority", "↑"),
  (".constructs.clothing_realism", ".character.is_token", "Token", "↓"),

  (".constructs.combined_ethnic_signals", ".character.gendergroup","women","↑"),
  (".constructs.combined_ethnic_signals", ".character.country", "Japan", "↓"),
  (".constructs.combined_ethnic_signals", ".character.is_token","Majority","↓"),
  (".constructs.combined_ethnic_signals", ".character.is_token", "Token", "↑"),

  (".constructs.admirableness", ".character.gendergroup", "women", "↓"),
  (".constructs.admirableness", ".character.country", "Japan", "↑"),

  (".constructs.positive_gender_rep", ".character.gendergroup", "women", "↓"),

  (".constructs.positive_ethnic_rep", ".character.country", "Japan", "↑"),
  (".constructs.positive_ethnic_rep", ".character.is_token", "Majority", "↑"),
  (".constructs.positive_ethnic_rep", ".character.is_token", "Token", "↓"),
]

def main(fin):
  """
  Analyze the data from stdin.
  """
  data = json.loads(fin.read())
  records = data["records"]
  fields = data["fields"]
  rows = []
  for r in records:
    row = { fields[i]: r[i] for i in range(len(fields)) }
    rows.append(row)

  print('='*80)
  print("Starting statistical analysis...")
  print('-'*80)
  tests = init_tests(rows, hypotheses)
  analyze_tests(rows, tests)
  print('-'*80)
  analyze_agreement(rows)
  print('-'*80)
  print("...analysis complete.")
  print('='*80)

def init_tests(rows, hypotheses):
  """
  Constructs a bunch of test objects and returns a list of them for
  analyze_tests to process.
  """
  result = []
  # TODO
  return result

def analyze_tests(rows, tests):
  """
  Given a bunch of test objects, analyzes them and prints out results.
  """
  for t in tests:
    print(t)
    # TODO

def analyze_agreement(rows):
  n_raters = len(rows)//5
  n_characters = len(rows)//7
  print("Rating agreement (full/categorical):")
  for t in test_agreement:
    ratings = np.full((n_raters, n_characters), np.nan)
    bin_ratings = np.full((n_raters, n_characters), np.nan)
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
      val = get(row, t)
      ratings[pid,cid] = val
      bin_ratings[pid,cid] = [-1,0,1][(val>3) + (val>4)] if val else None
    # DEBUG:
    """
    if "muscular" in t:
      rgrouped = {i: [] for i in range(len(characters))}
      bingrouped = {i: { -1: 0, 0: 0, 1: 0 } for i in range(len(characters))}
      for pid in range(ratings.shape[0]):
        for cid in range(ratings.shape[1]):
          if not np.isnan(ratings[pid,cid]):
            rgrouped[cid].append(ratings[pid,cid])
          if not np.isnan(bin_ratings[pid,cid]):
            bingrouped[cid][bin_ratings[pid,cid]] += 1
      for i, ch in enumerate(characters):
        print(
          "{:>12s}: {} :: {}/{}/{}".format(
            ch,
            [int(x) for x in rgrouped[i]],
            bingrouped[i][-1],
            bingrouped[i][0],
            bingrouped[i][1],
          )
        )
    #"""
    α = kr_alpha(
      reliability_data = ratings,
      value_domain = list(range(7)),
      level_of_measurement = "ordinal"
    )
    α_binary = kr_alpha(
      reliability_data = bin_ratings,
      value_domain = [-1, 0, 1],
      level_of_measurement = "ordinal"
    )
    print(
      "  {:>22s}:  {:<8s} /   {:<8s}".format(
        t.split('.')[-1],
        "{:.3g}".format(α),
        "{:.3g}".format(α_binary)
      )
    )

if __name__ == "__main__":
  main(sys.stdin)
