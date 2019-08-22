#!/usr/bin/env python3
"""
find_holy.py

Finds rows of batch files where more than x% of answers are missing, and print
the corresponding worker IDs. It also prints the number of missing answers, the
total number of answer columns, and the HIT status for each row.
"""

import sys
import csv

THRESHOLD = 0.1

def main(filenames):
  for f in filenames:
    with open(f, 'r') as fin:
      reader = csv.DictReader(fin)
      for row in reader:
        answers = [k for k in row if k.startswith("Answer.")]
        missing = [row[k] for k in answers if row[k] in ["", "{}", None]]
        if len(missing) / len(answers) > THRESHOLD:
          print(
            row["WorkerId"],
            len(missing),
            len(answers),
            row["AssignmentStatus"],
            sep='\t'
          )

if __name__ == "__main__":
  targets = sys.argv[1:]
  main(targets)
