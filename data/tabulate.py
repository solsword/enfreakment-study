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

def make_table(table_spec):
  """
  Turns a table specification into a LaTeX table string. Uses the
  TABLE_FMT template. The table_spec should be a dictionary with the
  following entries:

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

def get_hypothesis(component, category):
  """
  Looks up a hypothesis about a particular construct and category. The
  category must be the primary category for the hypothesis, not the
  secondary or alternate category.
  """
  # TODO: reverse-polarity framedata hypotheses!
  for hyp in analyze.all_hypotheses:
    key, construct, pos, neg, direction = hyp[:5]
    if construct == component and pos == category:
      return hyp
  # No matching hypothesis
  return None

def get_row_data(effects, expected, table, which_row):
  """
  Given effects/expected results and a table, looks up the data for the
  wich_rowth row of the table.
  """
  component = table["row_components"][which_row]
  result = []
  for category in table["col_categories"]:
    hyp = get_hypothesis(component, category)
    if hyp == None:
      result.append(r"\nh") # no hypothesis
      continue
    test_key = hyp[0]
    ef = effects.get(test_key, "missing")
    exp = expected.get(test_key, "missing")
    if ef == "missing" or exp == "missing":
      print(
        "Warning: missing effect/expected data for hypothesis: '{}'.".format(
          test_key
        ),
        file=sys.stderr
      )
      result.append(r"\nh") # no hypothesis
      continue # no data available
    if isinstance(ef, (int, float)) and ef > 0:
      if exp:
        result.append(r"\gt") # expectedly greater than
      else:
        result.append(r"\ug") # unexpectedly greater than
    elif isinstance(ef, (int, float)) and ef < 0:
      if exp:
        result.append(r"\lt") # expectedly less than
      else:
        result.append(r"\ul") # unexpectedly less than
    else:
      if hyp[4] == '+':
        result.append(r"\Ng") # NOT greater than
      else:
        result.append(r"\Nl") # NOT less than

  return result

def show_tables(effects, expected):
  """
  Prints out LaTeX table(s) and caption(s).
  """
  # TODO: TABLE2
  data = {}
  n_hyp = 0
  for i, row in enumerate(TABLE1["rows"]):
    if row == MIDRULE:
      continue
    data[row] = get_row_data(effects, expected, TABLE1, i)
    for dt in data[row]:
      if dt != r"\nh":
        n_hyp += 1

  tspec = {}
  tspec.update(TABLE1)
  tspec["data"] = data

  print(make_table(tspec))
  print(CAPTION1.format(n_hyp=n_hyp))


def main(json_string):
  effects, expected = json.loads(json_string)
  show_tables(effects, expected)

if __name__ == "__main__":
  main(sys.stdin.read())
