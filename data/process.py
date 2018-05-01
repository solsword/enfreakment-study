#!/usr/bin/env python3

import csv
import sys

import properties

idfields = [
  "Answer.id_1",
  "Answer.id_2",
  "Answer.id_3",
  "Answer.id_4",
  "Answer.id_5",
]

normalize_case = [
  "gender_description",
  "lang_primary",
  "lang_secondary",
  "lang_tertiary",
]

normalize_map = {
  "suitable": {
    "": "",
    None: "yes"
  },
  "ethnicity_description":{
    "NO": "Unknown",
    "i like very so match this task and very happy thank you.": "Unknown",
    "asian": "Asian",
    "Asian": "Asian",
    "ASIAN": "Asian",
    "indian": "Indian",
    "hispanic": "Hispanic",
    "black": "Black",
    "Black": "Black",
    "African American": "African American",
    "caucasian": "Caucasian Unknown",
    "Caucasion": "Caucasian Unknown",
    "Caucasian": "Caucasian Unknown",
    "caucasion": "Caucasian Unknown",
    "Caucasian white": "Caucasian Unknown",
    "Caucasian/white": "Caucasian Unknown",
    "Caucasian White": "Caucasian Unknown",
    "White-Caucasian": "Caucasian Unknown",
    "White/Caucasian": "Caucasian Unknown",
    "White/ Caucasian": "Caucasian Unknown",
    "White, caucasian": "Caucasian Unknown",
    "Non-Hispanic White": "Caucasian Unknown",
    "white": "Caucasian Unknown",
    "White": "Caucasian Unknown",
    "White Caucasian": "Caucasian Unknown",
    "White-Caucasian": "Caucasian Unknown",
    "White American": "Caucasian American",
    "White American, third generation(not \"European\")": "Caucasian American",
    "White, North American": "Caucasian American",
    "American": "Caucasian American",
    "White European": "Caucasian European",
    "I am half German and half English. I just consider myself to be Anglo/Saxon or just White.": "Caucasian European",
    "White/Caucasian, West European Descent": "Caucasian European",
    "euro-white": "Caucasian European",
    "White (European American) non-hispanic": "Caucasian American",

  },
  "nationality_description":{
    "American": "United States of America",
    "american": "United States of America",
    "American, USA": "United States of America",
    "I am American.": "United States of America",
    "united states": "United States of America",
    "United States": "United States of America",
    "United States of America": "United States of America",
    "US": "United States of America",
    "usa": "United States of America",
    "USA": "United States of America",
    "USA!": "United States of America",
    "USA-- born and raised here": "United States of America",
    "ianda": "Indian",
    "india": "Indian",
    "India": "Indian",
    "INDIA": "Indian",
    "indian": "Indian",
    "INDIAN": "Indian",
    "Indian": "Indian",
  },
}

CPROPS = None
CPFILE = "all_chars.csv"

def define_cprops():
  """
  Defines character properties from the CPFILE.
  """
  global CPROPS
  CPROPS = {}
  with open(CPFILE, 'r') as fin:
    reader = csv.DictReader(fin)
    for rin in reader:
      cid = rin["id"]
      CPROPS[cid] = rin

def cheat_char_prop(cid, prp):
  """
  Cheats by looking up a character property from the definitions file.
  """
  if CPROPS == None:
    define_cprops()

  uprp = properties.char_prop_untangle[prp]
  if uprp == "gender":
    return properties.gendergroups[CPROPS[cid][uprp]]
  else:
    return CPROPS[cid][uprp]

def process(sources):
  results = []
  results.append( # the header
    ["participant", "id"]
  + ["character_" + ch for ch in properties.character_properties]
  + properties.participant_properties
  + properties.ratings
  + properties.personal_ratings
  )
  rout = []
  results.append(rout)

  participant = 0 # track participant ID

  for fn in sources:
    with open(fn, 'r') as fin:
      reader = csv.DictReader(fin)

      for rin in reader:
        participant += 1
        for idf in idfields:
          n = idf[-1]
          cid = rin[idf]
          rout.append(participant)
          rout.append(cid)

          for ch in properties.character_properties:
            ikey = "Input.{}{}".format(ch,n)
            if ikey in rin:
              val = rin[ikey]
            else:
              cid = rin["Answer.id_{}".format(n)]
              val = cheat_char_prop(cid, ch)
            rout.append(val)

          for p in properties.participant_properties:
            pkey = "Answer.{}".format(p)
            if pkey in rin:
              val = rin[pkey]
            else:
              val = ""
            if val in ("{}", ""):
              val = None
            elif p in normalize_map:
              nm = normalize_map[p]
              if val in nm:
                val = nm[val]
              elif None in nm:
                val = nm[None]
              else:
                val = "<{}>".format(val)
            elif p in normalize_case:
              val = val.title()

            rout.append(val)

          for c in properties.ratings + properties.personal_ratings:
            val = rin["Answer.{}_{}".format(c, n)]

            if val in ("{}", ""):
              val = None
            else:
              try:
                val = int(val)
              except:
                print("Nonintable: {}='{}'".format(c, val), file=sys.stderr)

            rout.append(val)

          rout = []
          results.append(rout)

  return results

def output(results, dest=sys.stdout):
  for i in range(len(results)):
    last = i == len(results) - 1
    row = results[i]
    pure = [str(x) if x != None else "" for x in row]
    print('\t'.join(pure), end='\n' if not last else '', file=dest)

if __name__ == "__main__":
  d = process(sys.argv[1:])
  output(d, sys.stdout)
