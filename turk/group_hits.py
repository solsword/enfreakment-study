#!/usr/bin/env python3
"""
Reads groups.csv and all_chars.csv and prints out CSV lines suitable for input
into Amazon Mechanical Turk to instantiate template-likert.html.
"""

import csv
import sys

IMAGE_URLS = {
  "sfv": {
    "A": "http://web.mit.edu/pmwh/www/enfreakment-images/clean/sfv_cs_{}.jpg",
    "B": "http://web.mit.edu/pmwh/www/enfreakment-images/clean/sfv_oa_{}.jpg",
    "C": "http://web.mit.edu/pmwh/www/enfreakment-images/clean/sfv_ig_{}.jpg",
  },
  "tk7": {
    "A": "http://web.mit.edu/pmwh/www/enfreakment-images/clean/tk7_cs_{}.jpg",
    "B": "http://web.mit.edu/pmwh/www/enfreakment-images/clean/tk7_pr_{}.png",
    "C": "http://web.mit.edu/pmwh/www/enfreakment-images/clean/tk7_ig_{}.jpg",
  }
}
FLAG_URL = "http://web.mit.edu/pmwh/www/enfreakment-images/flags/{}.png"

GENDER_GROUPS = {
  "male": "men",
  "female": "women",
  "ambiguous_male": "men", # official male pronouns
  "ambiguous_female": "women", # official female pronouns
}

groups = []
with open("groups.csv", newline='') as fin:
  reader = csv.reader(fin)
  for row in reader:
    groups.append(row)

with open("all_chars.csv") as fin:
  raw = fin.readlines()

rows = []
keys = raw[0][:-1].split(',')
for raw_row in raw[1:]:
  bits = []
  while raw_row:
    if raw_row[0] == '"':
      eq = raw_row[1:].index('"')
      bits.append(raw_row[1:eq+1])
      raw_row = raw_row[eq+3:]
    else:
      if ',' in raw_row:
        ni = raw_row.index(',')
        bits.append(raw_row[:ni])
        raw_row = raw_row[ni+1:]
      else:
        bits.append(raw_row[:-1])
        raw_row = ''

  if len(bits) != len(keys):
    print(
      "Error: wrong number of bits ({} != {}):\n{}".format(
        len(bits),
        len(keys),
        ','.join(bits)
      ),
      file=sys.stderr
    )
  rows.append({})
  for i in range(len(keys)):
    rows[-1][keys[i]] = bits[i]

nr = len(rows)

#for gr in groups:
#  print(", ".join(rows[i-1]["name"] for i in gr))

#print("Groupings:", len(groups))

head = (
  "id1,name1,shortname1,namepossessive1,imageA1,imageB1,imageC1,"
  "country1,gender1,gendergroup1,bio1,quote1,"
)
head += (
  "id2,name2,shortname2,namepossessive2,imageA2,imageB2,imageC2,"
  "country2,gender2,gendergroup2,bio2,quote2,"
)
head += (
  "id3,name3,shortname3,namepossessive3,imageA3,imageB3,imageC3,"
  "country3,gender3,gendergroup3,bio3,quote3,"
)
head += (
  "id4,name4,shortname4,namepossessive4,imageA4,imageB4,imageC4,"
  "country4,gender4,gendergroup4,bio4,quote4,"
)
head += (
  "id5,name5,shortname5,namepossessive5,imageA5,imageB5,imageC5,"
  "country5,gender5,gendergroup5,bio5,quote5"
)

print(head)

for gr in groups:
  line = ""
  for cid in gr:
    selected = None
    for r in rows:
      if r["id"] == cid:
        selected = r
        break
    if selected == None:
      print(
        "Error: Character '{}' does not exist!".format(cid),
        file=sys.stderr
      )
    iubase = IMAGE_URLS[selected["game"]]
    line+=(
      '{id},{fn},{nm},{np},{imA},{imB},{imC},{co},{gd},{gg},"{bi}","{qu}",'
    ).format(
      id=selected["id"],
      fn=selected["name"],
      nm=selected["shortname"],
      np=selected["possessive"],
      imA=iubase["A"].format(selected["id"]), # character select
      imB=iubase["B"].format(selected["id"]), # official art
      imC=iubase["C"].format(selected["id"]), # in-game
      co=selected["country"],
      gd=selected["gender"],
      gg=GENDER_GROUPS[selected["gender"]],
      bi=selected["bio"],
      qu=selected["quote"]
    )
  print(line[:-1]) # remove trailing comma
