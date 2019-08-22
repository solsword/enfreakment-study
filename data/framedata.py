"""
framedata.py

Reads in frame data from framedata.json file.

Run make in ../framedata to produce framedata.json file and copy it over
manually.
"""

import json

def parse_frame_data():
  """
  Parses the frame data and returns a mapping from character IDs to mappings
  from stat name to stat value.
  """
  result = None
  with open("framedata.json", 'r') as fin:
    result = json.load(fin)

  return result
