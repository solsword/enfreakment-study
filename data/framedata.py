"""
framedata.py

Reads in frame data from framedata.tsv file.

Run make in ../framedata to produce framedata.tsv file and copy it over
manually.
"""

import csv

def parse_frame_data():
  """
  Parses the frame data and returns a mapping from character IDs to mappings
  from stat name to stat value.
  """
  result = {}
  with open("framedata.tsv", 'r') as fin:
    reader = csv.DictReader(fin, dialect="excel-tab")
    for row in reader:
      result[row["id"]] = row
      del result[row["id"]]["id"] # redundant
  return result
