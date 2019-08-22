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

class Undefined:
  pass

# Note: Keep these in sync
normalized_properties = [
  "any_suitable",
  "normalized_gender",
  "normalized_ethnicity",
  "normalized_nationality"
]

normalize_map = {
  "suitable": {
    "": "",
    Undefined: "yes"
  },
  "gender_description":{
    "Male": "Male",
    "M": "Male",
    "Female": "Female",
    "Female.": "Female",
    "Agender": "Agender",
    "25": "Unknown",
    None: "Unknown",
  },
  "ethnicity_description":{
    "": "Unknown",
    "No": "Unknown",
    "Yes": "Unknown",
    "Nothing": "Unknown",
    "Na": "Unknown",
    "N/A": "Unknown",
    "Male": "Unknown",
    "Possible No": "Unknown",
    "I Like Very So Match This Task And Very Happy Thank You.": "Unknown",
    "Indian": "Indian",
    "Hispanic": "Hispanic",
    "Spanic": "Hispanic",
    "Latino": "Latinx",
    "Latina": "Latinx",
    "I Am A White Latino": "Latinx + White",
    "Mexican American": "Mexican + American",
    "Mixed-Black/White/Latino": "Black + Latinx + White",
    "Hispanic And White": "Hispanic + White",
    "White, Hispanic": "Hispanic + White",
    "Hispnic": "Hispanic",
    "White/Hispanic": "Hispanic + White",
    "White/Hispanic- American": "Hispanic + American + White",
    "Hispanic- Puerto Rican, Caucasian": "Hispanic + Puerto Rican + White",
    "Hispanic-Mexican American": "Hispanic + Mexican + American",
    "Black": "Black",
    "I Am Black Racial Group": "Black",
    "African American": "American + Black",
    "Black African American": "American + Black",
    "Caucasian": "White",
    "Caucasian, White": "White",
    "Caucasian / White , Non Hispanic": "White",
    "Caucasion": "White",
    "White": "White",
    "Caucasian White": "White",
    "Caucasian/White": "White",
    "White-Caucasian": "White",
    "White/Caucasian": "White",
    "White/Caucasican": "White",
    "White/ Caucasian": "White",
    "White, Caucasian": "White",
    "White (Caucasian)": "White",
    "Non-Hispanic White": "White",
    "White, Non-Hispanic": "White",
    "Non-Hispanic Caucasian": "White",
    "Non-Hispanic Caucasian, White": "White",
    "Caucasian, Not Hispanic Or Latino.": "White",
    "Caucasian Of Mixed European Decent": "White",
    "White Caucasian": "White",
    "White-Caucasian": "White",
    "White/Caucasian, West European Descent": "White",
    "I Am Half German And Half English. I Just Consider Myself To Be Anglo/Saxon Or Just White.": "German + English + White",
    "White American": "American + White",
    "American White Caucasian": "American + White",
    "White/American/Non-Hispanic": "American + White",
    "White American, Third Generation(Not \"European\")": "American + White",
    "White, North American": "American + White",
    "American": "American",
    "European": "European",
    "European Caucasian": "European + White",
    "European White": "European + White",
    "European, Caucasian": "European + White",
    "European - German, Uk, Irish": "European + German + Irish + English",
    "European American White": "European + American + White",
    "Caucasian / European": "European + White",
    "Caucasian (European)": "European + White",
    "White/Caucasian/European": "European + White",
    "White European": "European + White",
    "White, European-American": "European + American + White",
    "White European Decent": "European + White",
    "Euro-White": "European + White",
    "White (European American) Non-Hispanic": "European + American + White",
    "Asian, Hispanic, White": "Asian + Hispanic + White",
    "Asian": "Asian",
    "Asian.": "Asian",
    "Asian American": "Asian + American",
    "Asian-American": "Asian + American",
    "Asian, Korean": "Korean + Asian",
    "East Asian/ Korean.": "Korean + Asian",
    "Korean/Persian": "Korean + Persian",
    "South Asian": "Southeast Asian",
    "South East Asian": "Southeast Asian",
    "Chinese/Vietnamese": "Chinese + Vietnamese",
    "Vietnamese": "Vietnamese",
    "Southeast Asian, Vietnamese": "Southeast Asian + Vietnamese",
    "Vietmamese": "Vietnamese",
    "Chinese": "Chinese",
    "Black And White": "Black + White",
    "Black & White": "Black + White",
    "Black And White (Biracial)": "Black + White",
    "American, Hawaiian, Native American": "American + Hawaiian + Native American",
    "Caucasian (Irish, Scottish, English, French), Native American": "Native American + White + Irish + Scottish + English + French",
    "Native American": "Native American",
    "American Indian": "Native American",
    "White And Cherokee": "Native American + White",
    "White, Black, Native": "Native American + Black + White",
    "Caucasian (Uk And German) And Native American (One Set Of Great Grandparents)": "Native American + English + German + White",
    "White. Finnish-American": "Finnish + American + White",
    "White/Japanese": "Japanese + White",
    "White/Korean": "Korean + White",
    "White/Asian(Chinese)": "Asian + Chinese + White",
    "Caucasian, Japanese 25%": "Japanese + White",
    "White - German/Italian": "German + Italian + White",
    "American/Italian/German/Spanish": "American + Italian + German + Spanish",
    "American, Italian, Russian": "American + Italian + Russian",
    "White, German/Polish": "German + Polish + White",
    "White (Irish-German)": "German + Irish + White",
    "Caucasian - French And English": "English + French + White",
    "Caucasian/German": "German + White",
    "Caucasian/Italian.": "Italian + White",
    "White, Italian/French/Polish": "Italian + French + Polish + White",
    "White, Of Irish/Scottish Ancestry": "Irish + Scottish + White",
    "German, French, English": "German + French + English",
    "White English-Irish American": "Irish + English + American + White",
    "Scottish/German": "Scottish + German",
    "Hindu": "Hindu",
    "Yes I'M A Hindu": "Hindu",
    "Asian, South Indian": "Indian + Asian",
    "Indian, Asian": "Indian + Asian",
    "White Jewish American": "Jewish + American + White",
    "Yes,(1.Asian,2.American,3.African)": "American + Asian + African",
    "African American And Asian": "Black + Asian",
    "African American, West Indian": "Black + West Indian",
    "Black, Filipino": "Filipino + Black",
    "Filipino": "Filipino",
    "Filipino/Portuguese/Native Hawaiian": "Filipino + Portuguese + Hawaiian",
    "Black/Native American": "Native American + Black",
    "Greek": "Greek",
    "Irish, English And Russian": "Irish + English + Russian",
    "Irish, German, Swedish, English": "Irish + German + Swedish + English",
    "Irish & Italian": "Irish + Italian",
    "White Mid-Western Protestant": "American + White + Protestant",
    None: None,
  },
  "nationality_description":{
    "American Indian": "Native American",
    "American": "US American",
    "Amefican": "US American",
    "American.": "US American",
    "American; Black": "US American",
    "American (Us)": "US American",
    "American (Usa)": "US American",
    "American, Usa": "US American",
    "United States American": "US American",
    "Us Citizen": "US American",
    "Usian": "US American",
    "Us White": "US American",
    "White (United States)": "US American",
    "U.S": "US American",
    "African American": "US American",
    "American European": "US American + European",
    "European American": "US American + European",
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
    "India.": "Indian",
    "Indian": "Indian",
    "Indai": "Indian",
    "North American": "US American + Canadian",
    "Canadian": "Canadian",
    "Colombian": "Columbian",
    "Brazilian": "Brazilian",
    "Chilean": "Chilean",
    "Filipino": "Filipino",
    "Dutch/Scottish": "Dutch + Scottish",
    "French": "French",
    "Italian": "Italian",
    "Italian/Irish": "Italian + Irish",
    "Spanish": "Spanish",
    "Usa/Spain": "US American + Spanish",
    None: None,
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

WHY = None
WHYFILE = "why.tsv"

def define_why():
  """
  Defines motivations from the WHYFILE.
  """
  global WHY
  WHY = {}
  with open(WHYFILE, 'r') as fin:
    reader = csv.DictReader(fin, dialect="excel-tab")
    for rin in reader:
      pid = rin["id"]
      gender = rin["gender"]
      origin = rin["origin"]
      motive = rin["motive"]
      motive_desc = rin["motive_description"]
      WHY[pid] = (motive, motive_desc, gender, origin)

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

  if WHY == None:
    define_why()

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
            if ch in properties.motive_properties:
              if cid in WHY:
                motive, motive_desc, gender, origin = WHY[cid]
                if ch == "motive":
                  val = motive
                elif ch == "motive_description":
                  val = motive_desc
                else:
                  raise ValueError("Unexpected motive property '{}'".format(ch))
              else:
                val = None
                print(
                  "Warning: Character '{}' doesn't have motives defined".format(
                    cid
                  ),
                  file=sys.stderr
                )
            elif ikey in rin:
              val = rin[ikey]
            else:
              val = cheat_char_prop(cid, ch)

            if ch == "gendergroup" and cid == "leo":
                val = "ambiguous" # refilter Leo's gender

            rout.append(val)

          for p in properties.participant_properties:

            if p in normalized_properties:
              # There's no input data for these, but their base property will
              # output two values
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
              elif Undefined in nm:
                nval = nm[Undefined]
              else:
                nval = "<{}>".format(orig_val)
              # We output a second column containing the normalized value
              rout.append(nval)

          for c in properties.ratings + properties.personal_ratings:
            val = rin["Answer.{}_{}".format(c, n)]

            if val in ("{}", "", ' '):
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
