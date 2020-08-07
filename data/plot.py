#!/usr/bin/env python3

import sys
import json

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from analyze import get

gender_colors = [
  "#9900bb",
  "#ffbb00",
  "#0066cc",
]

tone_colors = [
  "#ff88cc",
  "#ffcc77",
  "#88eeff"
]

demographics_colors = [
  "#339900",
  "#008844",
  "#001177",
  "#440088",
]

# Font setup
font = {
  "family": "DejaVu Sans",
  "stretch": "condensed",
  "size": 15,
}
matplotlib.rc('font', **font)

default_colors = gender_colors

def plot_construct_by_group(
  crows,
  construct,
  group_def,
  group_arrange=None,
  style={}
):
  """
  Plots median sexualization by gender.
  """
  scale = [i/2 for i in range(2,15)]

  groups = set([group_def(r) for r in crows])

  if group_arrange == None:
    group_arrange = [ (g, g) for g in groups ]

  values = {
    g: [
      get(r, ".med_constructs:{}".format(construct))
        for r in crows
        if group_def(r) == g
    ]
      for g in groups
  }

  bins = {
    g: [
      len([x for x in values[g] if x >= b - 0.25 and x < b + 0.25])
        for b in scale
    ]
      for g in groups
  }
  max_count = max([max(bins[g]) for g in groups])
  max_bins = [ max_count ]*len(scale)


  fig, ax = plt.subplots()
  index = np.arange(len(scale))
  ng = len(groups)
  bar_height = 1/ng

  orects = plt.barh(
    index,
    [x+1 for x in max_bins],
    1.0,
    color="white",
    alpha=0.3,
    ec="gray"
  )
  rects = [
    plt.barh(
      index + (bar_height*i - bar_height*(ng//2)),
      bins[g],
      bar_height,
      color=style.get("colors", default_colors)[i],
      label=alias
    )
    for (i, (g, alias)) in enumerate(group_arrange)
  ]

  plt.xlabel("Number of Characters")
  plt.ylabel(style.get("ylabel", "Median Value"))
  if "title" in style:
    plt.title(style["title"], pad=45)
  plt.yticks(index, [int(s) if int(s) == s else s for s in scale])
  plt.xticks(range(max_count+1),range(max_count+1))
  plt.xlim(0, max_count+0.5)
  plt.legend(
    loc=style.get("lpos", "lower left"),
    bbox_to_anchor=(0, 1.01),
    ncol=len(group_arrange),
    fontsize=14
  )

  plt.tight_layout()

def plot_ranges_by_group(
  crows,
  constructs,
  group_def,
  group_arrange=None,
  style={}
):
  """
  Plots ranges for multiple constructs separated by groups.
  """
  scale = [i/2 for i in range(2,15)]

  groups = set([group_def(r) for r in crows])

  if group_arrange == None:
    group_arrange = [ (g, g) for g in groups ]

  values = {
    g: [
      [
        get(r, ".med_constructs:{}".format(c))
          for r in crows
          if group_def(r) == g
      ]
        for c in constructs
    ]
      for g in groups
  }

  ranges = {
    g: [
      (min(cvs), max(cvs))
      for cvs in values[g]
    ]
      for g in groups
  }

  fig, ax = plt.subplots()
  index = np.arange(len(constructs))
  ng = len(group_arrange)
  bar_width = 1/ng
  sep = 0.2
  index = index * (1 + sep)
  min_height = 0.07

  rects = [
    plt.bar(
      index - 0.5 + bar_width*(i+1),
      [
        rng[1] - rng[0] if rng[1] > rng[0] else min_height
          for rng in ranges[g]
      ],
      bar_width,
      [
        rng[0] if rng[1] > rng[0] else rng[0] - min_height/2
          for rng in ranges[g]
      ],
      color=style.get("colors", default_colors)[i],
      label=alias
    )
    for (i, (g, alias)) in enumerate(group_arrange)
  ]

  plt.xlabel("Construct")
  plt.ylabel(style.get("ylabel", "Median Value"))
  if "title" in style:
    plt.title(style["title"], pad=45)
  plt.yticks(
    scale,
    [int(s) if int(s) == s else s for s in scale]
  )
  plt.xticks(index, style.get("clabels", index), fontsize=14, rotation=90)
  plt.xlim(index[0] - 0.5 - sep, index[-1] + 0.5 + sep)
  plt.legend(
    loc=style.get("lpos", "lower left"),
    bbox_to_anchor=(0, 1.01),
    ncol=len(group_arrange),
    fontsize=14
  )

  plt.tight_layout()

def plot_histograms_by_group(
  crows,
  constructs,
  group_def,
  group_arrange=None,
  style={}
):
  """
  Plots histograms for multiple constructs separated by groups.
  """
  scale = [i/2 for i in range(2,15)]

  groups = set([group_def(r) for r in crows])

  if group_arrange == None:
    group_arrange = [ (g, g) for g in groups ]

  values = {
    g: [
      [
        get(r, ".med_constructs:{}".format(c))
          for r in crows
          if group_def(r) == g
      ]
        for c in constructs
    ]
      for g in groups
  }

  ranges = {
    g: [
      (min(cvs), max(cvs))
      for cvs in values[g]
    ]
      for g in groups
  }

  widths = {
    g: [
      [
        len([val for val in cvs if abs(val - value) < 0.1])
      + 0.5 * len([val for val in cvs if abs(val - value) <= 0.25])
        for value in scale
      ]
        for cvs in values[g]
    ]
      for g in groups
  }

  maxwidth = max(
    max(
      max(bincounts)
      for bincounts in widths[g]
    )
    for g in groups
  )

  fig, ax = plt.subplots()
  index = np.arange(len(constructs)) - 0.5
  ng = len(group_arrange)
  group_width = 1/ng
  exaggerate = 1.3
  width_unit = group_width * exaggerate
  sep = 0.2
  index = index * (1 + sep)
  min_height = 0.07

  boxes = plt.bar(
    index + (0.5 * (1 + sep)), # x-positions
    scale[-1] + 1.5, # bar heights
    1 + sep, # bar width
    color="white",
    alpha=0.3,
    ec="gray"
  )

  rects = [
    plt.barh(
      scale, # bar y-positions
      [ width_unit * (cv / maxwidth) for cv in construct_values ], # bar widths
      0.46, # bar height
      [
        (index + group_width*(i+1))[j] # which column we're in
      - 0.5 * width_unit * (cv / maxwidth) # center within column
        for cv in construct_values
      ], # bar x-positions
      color=style.get("colors", default_colors)[i],
      label=alias if j == 0 else None
    )
    for (i, (g, alias)) in enumerate(group_arrange)
    for (j, construct_values) in enumerate(widths[g])
  ]

  plt.xlabel("Construct")
  plt.ylabel(style.get("ylabel", "Median Value"))
  if "title" in style:
    plt.title(style["title"], pad=45)
  plt.yticks(
    scale,
    [int(s) if int(s) == s else s for s in scale],
    fontsize=14
  )
  plt.ylim(scale[0] - 0.5, scale[-1] + 0.5)
  plt.xticks(
    index + 0.5*(1+sep),
    style.get("clabels", index),
    fontsize=11,
  )
  plt.xlim(index[0], index[-1] + 1 + sep)
  plt.legend(
    loc=style.get("lpos", "lower left"),
    bbox_to_anchor=(0, 1.01),
    ncol=len(group_arrange),
    fontsize=14
  )

  plt.tight_layout()

language_misspellings = {
  "Englsih": [ "English" ],
  "Hindhi": [ "Hindi" ],
  "Hidni": [ "Hindi" ],
  "hindhi": [ "Hindi" ],
  "hindi": [ "Hindi" ],
  "N/A": [],
  "n/a": [],
  "N/A (Only English)": [],
  "Na": [],
  "NA": [],
  "NILL": [],
  "nil": [],
  "NO": [],
  "No": [],
  "no": [],
  "None": [],
  "none": [],
  "NONE": [],
  "Spansh": [ "Spanish" ],
  "Spaines": [ "Spanish" ],
  "Italic": [ "Italian" ],
  "Italino": [ "Italian" ],
  "ARABIC": [ "Arabic" ],
  "FRENCH": [ "French" ],
  "french": [ "French" ],
  "HINDI AND TELUGU": ["Hindi", "Telugu"],
  "MALAYALAM": ["Malayalam"],
  "malayalam": ["Malayalam"],
  "THELUGU, MALAYALAM": ["Telugu", "Malayalam"],
  "tamil": ["Tamil"],
  "telgu": ["Telugu"],
}

value_orderings = {
  "Age": [
    ("18-24", "18-24"),
    ("25-34", "25-34"),
    ("35-44", "35-44"),
    ("45-54", "45-54"),
    ("55-64", "55-64"),
    ("65-74", "65-74"),
    ("75+", "75+"),
  ],
  # Original full prompt questions
  #"Education": [
  #  ('', "<no answer>"),
  #  ("primary", "Primary school (8th grade)"),
  #  ("some_high", "Some high school (no diploma)"),
  #  ("high", "High school (or equivalent, e.g., GED)"),
  #  ("technical", "Trade/technical/vocational training"),
  #  ("associate", "Associate degree"),
  #  ("some_college", "Some college (no degree)"),
  #  ("bachelors", "Bachelor's degree"),
  #  ("masters", "Master's degree"),
  #  ("doctorate", "Doctorate degree"),
  #],
  # Abbreviated for presentation
  "Education": [
    ('', "<no answer>"),
    ("primary", "Primary school"),
    ("some_high", "Some high school"),
    ("high", "High school"),
    ("technical", "Vocational training"),
    ("associate", "Associate degree"),
    ("some_college", "Some college"),
    ("bachelors", "Bachelor's degree"),
    ("masters", "Master's degree"),
    ("doctorate", "Doctorate degree"),
  ],
  "Play Frequency": [
    ("daily", "Daily"),
    ("weekly", "Weekly"),
    ("monthly", "Monthly"),
    ("infrequent", "Infrequently"),
    ("never", "Never"),
  ],
}

min_viable_height = 20
min_viable_width = 20
label_offset = 4

def label_bars(ax, rects, labels, vert=False):
  for rect, label in zip(rects, labels):
    if vert:
      h = rect.get_height()
      if h > min_viable_height:
        ax.text(
          rect.get_x() + rect.get_width()/2,
          h - label_offset,
          label,
          color="white",
          ha="center",
          va="top"
        )
      else:
        ax.text(
          rect.get_x() + rect.get_width()/2,
          h + label_offset,
          label,
          color="black",
          ha="center",
          va="bottom"
        )
    else:
      w = rect.get_width()
      if w > min_viable_width:
        ax.text(
          w - label_offset,
          rect.get_y() + rect.get_height()/2,
          label,
          color="white",
          ha="right",
          va="center"
        )
      else:
        ax.text(
          w + label_offset,
          rect.get_y() + rect.get_height()/2,
          label,
          color="black",
          ha="left",
          va="center"
        )


def plot_demographics(prows, style={}):
  """
  Plots demographic information all at once.
  """
  # Configure font size
  font = {
    "family": "DejaVu Sans",
    "stretch": "condensed",
    "size": 19,
  }
  matplotlib.rc('font', **font)

  simple_properties = [
    ("age", "Age", ".participant.age"),
    ("edu", "Education", ".participant.education"),
    ("play", "Play Frequency", ".participant.play_frequency"),
    ("gender", "Gender", ".participant.normalized_gender"),
    #("Ethnicity", ".participant.normalized_ethnicity"),
    #("Nationality", ".participant.normalized_nationality"),
  ]
  compound_properties = [
    (
      "played",
      "Games Played",
      [
        (".participant.played_specific", { "no" }),
        (".participant.played_franchise", { "no" }), 
        (".participant.played_fighting", { "no" }),
        (".participant.played_any", None), 
      ]
    ),
    (
      "watched",
      "Games Watched",
      [
        (".participant.watched_franchise", { "no" }),
        (".participant.watched_fighting", None),
      ]
    ),
  ]

  for i, (tag, name, pr) in enumerate(simple_properties):
    fig, ax = plt.subplots()
    if isinstance(get(prows[0], pr), dict):
      values = set()
      for r in prows:
        values |= set(get(r, pr).keys())
      values = sorted(list(values))
      order = (
        value_orderings[name]
          if name in value_orderings
          else [(v, v) for v in values]
      )
      hist = [
        len([r for r in prows if v in get(r, pr)])
          for (v, d) in order
      ]
    else:
      values = sorted(list(set(get(r, pr) for r in prows)))
      order = (
        value_orderings[name]
          if name in value_orderings
          else [(v, v) for v in values]
      )
      hist = [
        len([r for r in prows if get(r, pr) == v])
          for (v, d) in order
      ]

    index = np.arange(len(values))
    bar_height = 0.8
    rects = ax.barh(
      index,
      hist,
      bar_height,
      color=style.get("colors", default_colors)[i],
      label=name
    )
    label_bars(ax, rects, hist, vert=False)
    ax.set_title(name, fontsize=24, pad=8)
    ax.set_yticks(index)
    ax.set_yticklabels([d for (v, d) in order])
    ax.get_xaxis().set_visible(False)
    fig.patch.set_visible(False)
    plt.tight_layout()

    filename = f"plots/demo-{tag}.svg"
    print(f"Saving '{filename}'...")
    plt.savefig(filename, format="svg")
    plt.close()

  for tag, name, fallbacks in compound_properties:
    pass
    # TODO

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

  crows = []
  seen = set()
  for r in rows:
    cid = get(r, ".character.id")
    if cid not in seen:
      seen.add(cid)
      crows.append(r)

  prows = []
  seen = set()
  for r in rows:
    pid = get(r, ".participant.id")
    if pid not in seen:
      seen.add(pid)
      prows.append(r)

  plot_construct_by_group(
    crows,
    2,
    lambda r: get(r, ".character.gendergroup"),
    group_arrange=[
      ["men", "Men"],
      ["women", "Women"],
      ["ambiguous", "Ambiguous"],
    ],
    style={
      "title": "Sexualization by Gender",
      "ylabel": "Median Sexualization Construct",
      "colors": gender_colors,
    }
  )

  filename = "plots/sexualization_by_gender.svg"
  print(f"Saving '{filename}'...")
  plt.savefig(filename, format="svg")
  plt.close()

  plot_histograms_by_group(
    crows,
    [3, 4, 1, 0, 2, 8],
    lambda r: get(r, ".character.gendergroup"),
    group_arrange=[
      ["men", "Men"],
      ["women", "Women"],
      ["ambiguous", "Ambiguous"],
    ],
    style={
      "clabels": [
        "musculature",
        "thinness",
        "youth",
        "attractive-\nness",
        "sexualization",
        "attire\nsexualization"
      ],
      "title": "Construct Ranges by Gender",
      "ylabel": "Median Construct Values",
      "xlabel": "Construct (width shows # of characters)",
      "colors": gender_colors,
    }
  )
  filename = "plots/constructs_by_gender.svg"
  print(f"Saving '{filename}'...")
  plt.savefig(filename, format="svg")
  plt.close()

  plot_histograms_by_group(
    crows,
    [3, 4, 1, 0, 2, 8],
    lambda r: get(r, ".character.skin_tone"),
    group_arrange=[
      ["lighter", "Lighter"],
      ["darker", "Darker"],
      ["indeterminate", "Indeterminate"],
    ],
    style={
      "clabels": [
        "musculature",
        "thinness",
        "youth",
        "attractive-\nness",
        "sexualization",
        "attire\nsexualization"
      ],
      "title": "Construct Ranges by Skin Color",
      "ylabel": "Median Construct Values",
      "xlabel": "Construct (width shows # of characters)",
      "colors": tone_colors,
    }
  )

  filename = "plots/constructs_by_skin_color.svg"
  print(f"Saving '{filename}'...")
  plt.savefig(filename, format="svg")
  plt.close()

  plot_demographics(prows, {"colors": demographics_colors})

  plt.show()

if __name__ == "__main__":
  main(sys.stdin)
