#!/usr/bin/env python3
"""
tabulate.py

Reads in analysis results (JSON on stdin) and spits out LaTeX tables.
"""

import sys
import json

import analyze

TABLE_FMT = """\
\\begin{{tabular}}{{{col_layout}}}
  \\toprule
  {head_line} \\\\
  \\midrule
  {rows}
  \\bottomrule
\\end{{tabular}}
"""

CAPTION1 = """\
  \\caption{{The results of our {n_hyp} construct hypotheses: each row shows one construct, and each column lists a primary group that we compared against all non-members, or in the skin color cases, against darker-skinned characters (of the same gender). The values in each cell show whether that group had lower or higher scores as predicted (\\lt/\\gt), or unexpectedly (\\ul/\\ug), or whether we made no prediction about those groups for that construct (\\nh). In cases where results were insignificant, the direction of our hypothesis is indicated using (\\Nl/\\Ng).}}
"""

CAPTION2 = """\
  \\caption{{The results of our {n_hyp} participant hypotheses: each row shows one hypothesis. The value in each row shows whether the listed group had lower or higher scores as predicted (\\lt/\\gt), or unexpectedly (\\ul/\\ug) for the listed construct. In cases where results were insignificant, the direction of our hypothesis is indicated using (\\Nl/\\Ng).}}
"""

MIDRULE = r"\midrule"

def column_layout(table_spec):
  """
  Returns the column layout for a given table specification, based on the
  number of rows.
  """
  return 'r' + ' c'*len(table_spec["columns"])

def group_line(table_spec):
  """
  The groups of a table_spec should be a list of strings, or pairs
  containing a string and a number of items for groups that span multiple
  columns. They need to line up against the columns or you'll run into
  trouble.
  """
  groups = table_spec["groups"]
  return " & ".join(
    [' ']
  + [
      (
        g
          if isinstance(g, str)
          else "\\multicolumn{{{cols}}}{{c}}{{{group}}}".format(
            cols=g[1],
            group=g[0]
          )
      )
      for g in groups
    ]
  )

def head_line(table_spec, rotated=True):
  """
  The columns of a table spec should be a list of strings. The length
  should match the sum of the column span of the groups, if groups are
  used. The result here will include the grouping line if groups are
  present.
  """
  tmpl = "{x}"
  if rotated: tmpl = "\\rhead{{{x}}}"
  cols = table_spec["columns"]
  result = " & ".join(
    [' ']
  + [
      tmpl.format(x=col)
        for col in cols
    ]
  )
  if "groups" in table_spec:
    gline = group_line(table_spec)
    return gline + ' \\\\\n  \\midrule\n' + result
  else:
    return result

def make_row(label, row_items, align=None):
  """
  Takes a label and row data and returns a row string.
  """
  if align:
    lbl = ' '*(align - len(label)) + label + ' '
  else:
    lbl = label + ' '
  return '&'.join([lbl] + row_items) + r'\\'

def make_rows_table(table_spec):
  """
  Turns a table specification into a LaTeX table string. Uses the
  TABLE_FMT template. This version creates a table that has a single
  column of hypothesis results, with two columns that specify the
  relevant grouping and the value being tested. The table_spec should be
  a dictionary with the following entries:

    'columns': A list of exactly three strings labelling the columns.
    'rows': A list of pairs strings specifying the contents of the first
      two columns of each row.
    'data': A list of strings to be placed in the third column; should
      have the same number of entries as the rows.
  """
  rows = []
  align = max(len(r[0]) for r in table_spec["rows"] if r != MIDRULE)
  for i, rinfo in enumerate(table_spec["rows"]):
    if isinstance(rinfo, (list, tuple)):
      group, construct = rinfo
      result = table_spec["data"][i]
    else:
      result = None

    if result == None:
      rows.append(rinfo)
    else:
      rows.append(make_row(group, [construct, result], align))

  hline = make_row(table_spec["columns"][0], table_spec["columns"][1:], align)
  hline = hline[:-2] # get rid of ending \\

  return TABLE_FMT.format(
    col_layout="r c c",
    head_line=hline,
    rows='\n  '.join(rows)
  )

def make_cross_table(table_spec):
  """
  Turns a table specification into a LaTeX table string. Uses the
  TABLE_FMT template. This version creates a matrix-style table with rows
  and columns where each cell represents a single hypothesis. The
  table_spec should be a dictionary with the following entries:

    'rows': A list of strings labelling the rows.
    'data': A dictionary mapping row labels to lists of strings.
    'columns': A list of strings labelling the columns. The length of
      each data list must match the number of columns exactly.
    'groups': A list of strings, or tuples containing a string and a
      number. A string just "groups" one column, while a string with a
      number groups that many columns. If groups is not present, no
      groups will appear in the table.
  """
  rows = []
  align = max(len(r) for r in table_spec["rows"] if r != MIDRULE)
  for row in table_spec["rows"]:
    rdata = table_spec["data"].get(row)
    if rdata == None:
      rows.append(row)
    else:
      rows.append(make_row(row, rdata, align))

  hline = head_line(table_spec, rotated=table_spec.get("rotate_headers"))

  return TABLE_FMT.format(
    col_layout=column_layout(table_spec),
    head_line=hline,
    rows='\n  '.join(rows)
  )

# Table reporting the by-character construct hypothesis results
TABLE1 = {
  "rotate_headers": True,
  "groups": [
    "Gender",
    "Skin Color",
    ("National Origin", 4),
    ("Intersections", 4)
  ],
  "columns": [
    "Female",
    "Lighter-skinned",
    "Japanese",
    "Majority",
    "Token",
    "Unknown",
    "Lighter Female",
    "Majority female",
    "Lighter male",
    "Majority male"
  ],
  # Actual items used for finding hypotheses:
  "col_categories": [
    analyze.character_female,
    analyze.is_lighter_skinned,
    analyze.is_japanese,
    analyze.is_majority,
    analyze.is_token,
    analyze.unknown_country,
    analyze.lighter_skinned_women,
    analyze.majority_women,
    analyze.lighter_skinned_men,
    analyze.majority_men,
  ],
  "rows": [
    "body realism",
    "attire realism",
    "ethnic cues",
    MIDRULE,
    "musculature",
    "body type",
    "youth",
    "attractiveness",
    "sexualization",
    "attire sxlztn.",
    MIDRULE,
    "admirability",
    "ethnic rep.",
    "gender rep.",
  ],
  # Actual items used for finding hypotheses:
  "row_components": [
    ".constructs.body_realism",
    ".constructs.clothing_realism",
    ".constructs.combined_ethnic_signals",
    None,
    ".constructs.muscles",
    ".constructs.thinness",
    ".constructs.youth",
    ".constructs.attractiveness",
    ".constructs.sexualization",
    ".constructs.attire_sexualization",
    None,
    ".constructs.admirability",
    ".constructs.positive_ethnic_rep",
    ".constructs.positive_gender_rep",
  ],
}

# Table reporting the by-participant construct hypothesis results
TABLE2 = {
  "rotate_headers": False,
  # No groups
  "columns": [
    "Group",
    "Construct",
    "Result",
  ],
  "rows": [
    ("Women", "Gender representation"),
    ("Infrequent game-players", "Gender representation"),
    ("Frequent game-players", "Gender representation"),
    MIDRULE,
    ("When ethnicities are similar", "Ethnic representation"),
    ("Nonwhite participants", "Ethnic representation"),
    ("Infrequent game-players", "Ethnic representation"),
    ("Frequent game-players", "Ethnic representation"),
  ],
  # Actual items used for finding hypotheses:
  "hypothesis_categories": [
    (analyze.participant_female, ".constructs.positive_gender_rep"),
    (analyze.infrequent_player, ".constructs.positive_gender_rep"),
    (analyze.frequent_player, ".constructs.positive_gender_rep"),
    None,
    (analyze.ethnically_similar, ".constructs.positive_ethnic_rep"),
    (analyze.participant_nonwhite, ".constructs.positive_ethnic_rep"),
    (analyze.infrequent_player, ".constructs.positive_ethnic_rep"),
    (analyze.frequent_player, ".constructs.positive_ethnic_rep"),
  ],
}

hypotheses_requested = set()

def get_hypothesis(component, category):
  """
  Looks up a hypothesis about a particular construct and category. The
  category must be the primary category for the hypothesis, not the
  secondary or alternate category.
  """
  global hypotheses_requested
  for hyp in analyze.all_hypotheses:
    key, construct, pos, neg, direction = hyp[:5]
    if construct == component and pos == category:
      hypotheses_requested.add(hyp[:5])
      return hyp
  # No matching hypothesis
  return None

def get_cross_row_data(effects, expected, table, which_row):
  """
  Given effects/expected results and a table, looks up the data for the
  wich_rowth row of the table.
  """
  component = table["row_components"][which_row]
  result = []
  for category in table["col_categories"]:
    result.append(get_test_result(effects, expected, category, component))

  return result

def get_test_result(effects, expected, group, construct):
  hyp = get_hypothesis(construct, group)
  return get_hypothesis_result(hyp, effects, expected)

def get_hypothesis_result(hypothesis, effects, expected):
    if hypothesis == None:
      return r"\nh" # no hypothesis
    test_key = hypothesis[0]
    ef = effects.get(test_key, "missing")
    exp = expected.get(test_key, "missing")
    if ef == "missing" or exp == "missing":
      print(
        "Warning: missing effect/expected data for hypothesis: '{}'.".format(
          test_key
        ),
        file=sys.stderr
      )
      return r"\nh" # no hypothesis
    if isinstance(ef, (int, float)) and ef > 0:
      if exp:
        return r"\gt" # expectedly greater than
      else:
        return r"\ug" # unexpectedly greater than
    elif isinstance(ef, (int, float)) and ef < 0:
      if exp:
        return r"\lt" # expectedly less than
      else:
        return r"\ul" # unexpectedly less than
    else:
      if hypothesis[4] == '+':
        return r"\Ng" # NOT greater than
      else:
        return r"\Nl" # NOT less than

def show_tables(effects, expected):
  """
  Prints out LaTeX table(s) and caption(s).
  """
  data = {}
  n_hyp = 0
  for i, row in enumerate(TABLE1["rows"]):
    if row == MIDRULE:
      continue
    data[row] = get_cross_row_data(effects, expected, TABLE1, i)
    for dt in data[row]:
      if dt != r"\nh":
        n_hyp += 1

  tspec = {}
  tspec.update(TABLE1)
  tspec["data"] = data

  print(make_cross_table(tspec))
  print(CAPTION1.format(n_hyp=n_hyp))

  data2 = []
  for i, hinfo in enumerate(TABLE2["hypothesis_categories"]):
    if hinfo != None:
      group, construct = hinfo
      data2.append(get_test_result(effects, expected, group, construct))
    else:
      data2.append(None)

  tspec2 = {}
  tspec2.update(TABLE2)
  tspec2["data"] = data2

  print('-'*80)
  print()

  print(make_rows_table(tspec2))
  print(CAPTION2.format(n_hyp=len(list(filter(lambda x: x != None, data2)))))

  unrequested = [
    hyp[0]
    for hyp in analyze.all_hypotheses
    if hyp[:5] not in hypotheses_requested
  ]

  if unrequested:
    print('-'*80)
    print("Hypotheses not in any table:")
    for hyp_id in unrequested:
      print(hyp_id)


def main(json_string):
  effects, expected = json.loads(json_string)
  show_tables(effects, expected)

if __name__ == "__main__":
  main(sys.stdin.read())
