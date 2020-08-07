#!/usr/bin/env python3

import json
import numpy as np
from krippendorff import alpha as kr_alpha

import analyze

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

def analyze_tests(rows, tests, threshold = 0.05):
  """
  Given a bunch of test objects, analyzes them and prints out results.
  """
  failed = False
  m = len(tests)
  effects = {}
  expected = {}
  for i, (name, expd, md, p, smsg, fmsg) in enumerate(
    sorted(tests, key=lambda x: x[3])
  ):
    k = i + 1
    #th = threshold / (m - i) ## Holm-Bonferroni
    th = threshold * (k/m) # Benjamini-Hochberg
    error = md == None
    close = p < threshold if not isinstance(p, str) else False
    expected[name] = expd
    if error:
      e = "ERR: {}".format(fmsg)
      effects[name] = e
      print(e)
    elif failed:
      effects[name] = None
      print("{} {} ~ {:.3g}".format(" *"[close], fmsg, th))
    elif p > th:
      effects[name] = None
      failed = True
      print("{} {} > {:.3g}".format(" *"[close], fmsg, th))
    else:
      effects[name] = md
      print("{} {} < {:.3g}".format(" *"[close], smsg, th))

  return effects, expected

def summarize_tests(effects, expected, hgroups):
  for name in hgroups:
    hypotheses = hgroups[name]
    print(name)
    for hyp in hypotheses:
      if expected[hyp] == None:
        print("  {}: {}".format(hyp, effects[hyp]))
      else:
        print(
          "  {} {}: {}".format(
            ' ' if expected[hyp] else '!',
            hyp,
            "{:+.3g}".format(effects[hyp]) if effects[hyp] != None else '?'
          )
        )

def analyze_agreement(rows):
  n_raters = len(rows)//5
  n_characters = len(rows)//7
  print("Rating agreement (full/categorical):")
  for t in test_agreement:
    ratings = np.full((n_raters, n_characters), np.nan)
    bin_ratings = np.full((n_raters, n_characters), np.nan)
    pidmap = {}
    nextpid = 0
    for row in rows:
      pid = analyze.get(row, ".participant.id")
      if pid in pidmap:
        ipid = pidmap[pid]
      else:
        ipid = nextpid
        pidmap[pid] = ipid
        nextpid += 1
      ch = analyze.get(row, ".character.id")
      cid = analyze.charmap[ch]
      if not np.isnan(ratings[ipid, cid]):
        print(
          "Double-fill: [{}, {}] was {} ? {}!".format(
            ipid,
            ch,
            ratings[ipid, cid],
            np.isnan(ratings[ipid, cid])
          ),
          file=sys.stderr
        )
        print(row, file=sys.stderr)
      val = analyze.get(row, t)
      ratings[ipid,cid] = val
      bin_ratings[ipid,cid] = [-1,0,1][(val>3) + (val>4)] if val else None
    # DEBUG:
    """
    if "muscular" in t:
      rgrouped = {i: [] for i in range(len(characters))}
      bingrouped = {i: { -1: 0, 0: 0, 1: 0 } for i in range(len(characters))}
      for ipid in range(ratings.shape[0]):
        for cid in range(ratings.shape[1]):
          if not np.isnan(ratings[ipid,cid]):
            rgrouped[cid].append(ratings[ipid,cid])
          if not np.isnan(bin_ratings[ipid,cid]):
            bingrouped[cid][bin_ratings[ipid,cid]] += 1
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


def main(tests):
    rows = tests["rows"]
    tests = tests["tests"]

    suffix = ""
    if len(sys.argv) > 1:
        suffix = "-" + sys.argv[1]

    print('-'*80)
    print("Analyzing tests...")
    effects, expected = analyze_tests(rows, tests)
    # Dump into a file
    with open(f"analysis_results{suffix}.json", 'w') as fout:
      json.dump([effects, expected], fout)
    print('-'*80)
    summarize_tests(effects, expected, analyze.hgroups)
    print('-'*80)
    analyze_agreement(rows)
    print('-'*80)
    print("...analysis complete.")
    print('='*80)

if __name__ == "__main__":
    import sys
    inputs = json.load(sys.stdin)
    main(inputs)
