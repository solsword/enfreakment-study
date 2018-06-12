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
  "ethnicity_description",
  "nationality_description"
]

# Note: Keep these in sync
normalized_properties = [
  "any_suitable",
  "normalized_ethnicity",
  "normalized_nationality"
]
normalize_map = {
  "suitable": {
    "": "",
    None: "yes"
  },
  "ethnicity_description":{
    "No": "Unknown",
    "I Like Very So Match This Task And Very Happy Thank You.": "Unknown",
    "Asian": "Asian",
    "Indian": "Indian",
    "Hispanic": "Hispanic",
    "Latino": "Latinx",
    "I Am A White Latino": "Latinx + White",
    "Hispanic And White": "Hispanic + White",
    "White, Hispanic": "Hispanic + White",
    "White/Hispanic": "Hispanic + White",
    "White/Hispanic- American": "Hispanic + American + White",
    "Hispanic- Puerto Rican, Caucasian": "Hispanic + Puerto Rican + White",
    "Black": "Black",
    "African American": "Black",
    "Caucasian": "White",
    "Caucasion": "White",
    "White": "White",
    "Caucasian White": "White",
    "Caucasian/White": "White",
    "White-Caucasian": "White",
    "White/Caucasian": "White",
    "White/ Caucasian": "White",
    "White, Caucasian": "White",
    "Non-Hispanic White": "White",
    "White Caucasian": "White",
    "White-Caucasian": "White",
    "White/Caucasian, West European Descent": "White",
    "I Am Half German And Half English. I Just Consider Myself To Be Anglo/Saxon Or Just White.": "White",
    "White American": "American + White",
    "White American, Third Generation(Not \"European\")": "American + White",
    "White, North American": "American + White",
    "American": "American",
    "White European": "European + White",
    "Euro-White": "European + White",
    "White (European American) Non-Hispanic": "European + White",
    "Vietmamese": "Vietnamese",
    "Chinese": "Chinese",
    "Asian, Hispanic, White": "Asian + Hispanic + White",
    "Black And White (Biracial)": "Black + White",
    "American, Hawaiian, Native American": "American + Hawaiian + Native American",
    "Caucasian (Irish, Scottish, English, French), Native American": "Native American + White",
    "White/Japanese": "Japanese + White",
    "Caucasian, Japanese 25%": "Japanese + White",
    "German, French, English": "German + French + English",
    "Hindu": "Hindu",
    "Indian, Asian": "Indian + Asian",
    "Native American": "Native American",
    "White Jewish American": "Jewish + American + White",
    "Yes,(1.Asian,2.American,3.African)": "American + Asian + African",

  },
  "nationality_description":{
    "American Indian": "Native American",
    "American": "US American",
    "American, Usa": "US American",
    "American European": "US American + European",
    "Asian American": "US American",
    "I Am American.": "US American",
    "United States": "US American",
    "United States Of America": "US American",
    "Us": "US American",
    "Usa": "US American",
    "Usa!": "US American",
    "Usa-- Born And Raised Here": "US American",
    "Ianda": "Indian",
    "India": "Indian",
    "Indian": "Indian",
    "Canadian": "Canadian",
    "Colombian": "Columbian",
    "French": "French",
    "Usa/Spain": "US American + Spanish",
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

PIDS = None
PIDFILE = "pids.tsv"

def define_pids():
  """
  Defines anonymous participant IDs from the PIDFILE.
  """
  global PIDS
  PIDS = {}
  with open(PIDFILE, 'r') as fin:
    reader = csv.DictReader(fin, dialect="excel-tab")
    for rin in reader:
      pid = rin["id"]
      wid = rin["worker_id"]
      submissions = rin["submissions"]
      PIDS[wid] = (pid, submissions)

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
  if PIDS == None:
    define_pids()

  results = []
  ext_part_props = []
  results.append( # the header
    ["participant", "id"]
  + ["character_" + ch for ch in properties.character_properties]
  + properties.participant_properties
  + properties.ratings
  + properties.personal_ratings
  )
  rout = []
  results.append(rout)

  for fn in sources:
    with open(fn, 'r') as fin:
      if fn.endswith(".tsv"):
        reader = csv.DictReader(fin, dialect="excel-tab")
      else:
        reader = csv.DictReader(fin)

      for rin in reader:
        wid = rin["WorkerId"]
        if wid not in PIDS:
          raise ValueError("Unknown worker '{}'".format(wid))
        participant, submissions = PIDS[wid]
        submissions = int(submissions)

        if submissions > 1:
          continue # skip potentially tainted data

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

            if ch == "gendergroup" and cid == "leo":
                val = "ambiguous" # refilter Leo's gender

            rout.append(val)

          for p in properties.participant_properties:
            if p in normalized_properties:
              continue
            pkey = "Answer.{}".format(p)
            if pkey in rin:
              val = rin[pkey]
            else:
              val = ""

            orig_val = val

            if val in ("{}", ""):
              val = None
            elif p in normalize_case:
              val = val.title()

            rout.append(val)

            if p in normalize_map:
              nm = normalize_map[p]
              if val in nm:
                nval = nm[val]
              elif None in nm:
                nval = nm[None]
              else:
                nval = "<{}>".format(orig_val)
              rout.append(nval)

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
