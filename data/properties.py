"""
Properties.py

Code for dealing with character properties during data munging.
"""
 

character_properties = [
  "country",
  "gendergroup",
  "bio",
  "quote",
  #"skin_tone",
  "motive",
  "motive_description",
]

motive_properties = [
  "motive",
  "motive_description",
]

participant_properties = [
 "suitable",
 "any_suitable",
 "age",
 "education",
 "played_specific",
 "played_franchise",
 "played_fighting",
 "played_any",
 "play_frequency",
 "watched_franchise",
 "watched_fighting",
 "lang_primary",
 "lang_secondary",
 "lang_tertiary",
 "lang_extra",
 "gender_description",
 "ethnicity_description",
 "normalized_ethnicity",
 "nationality_description",
 "normalized_nationality",
 "feedback",
]

ratings = [
 "attire_ethnicity",
 "attire_not_sexualized",
 "attire_sexualized",
 "attractive",
 "chubby",
 "costume",
 "ethnic_stereotypes",
 "exaggerated_body",
 "gender_stereotypes",
 "muscular",
 "non_muscular",
 "not_role_model",
 "not_sexualized",
 "obv_ethnicity",
 "old",
 "pos_ethnic_rep",
 "pos_gender_rep",
 "realistic_body",
 "realistic_clothing",
 "role_model",
 "sexualized",
 "skinny",
 "ugly",
 "young",
]

personal_ratings = [
  "similarity",
  "ethnic_match",
  "ethnic_familiarity",
]


constructs = {
  "attractiveness": ["attractive", "-ugly"],
  "youth": ["young", "-old"],
  "sexualization": ["sexualized", "-not_sexualized"],
  "muscles": ["muscular", "-non_muscular"],
  "thinness": ["skinny", "-chubby"],
  "body_realism": ["realistic_body", "-exaggerated_body"],
  "clothing_realism": ["realistic_clothing", "-costume"],
  "combined_realism": [
    "realistic_body",
    "-exaggerated_body",
    "realistic_clothing",
    "-costume"
  ],
  "attire_sexualization": ["attire_sexualized", "-attire_not_sexualized"],
  "combined_sexualization": [
    "sexualized",
    "attire_sexualized",
    "-not_sexualized",
    "-attire_not_sexualized"
  ],
  "combined_ethnic_signals": ["attire_ethnicity", "obv_ethnicity"],
  "positive_gender_rep": ["pos_gender_rep", "-gender_stereotypes"],
  "positive_ethnic_rep": ["pos_ethnic_rep", "-ethnic_stereotypes"],
  "admirability": ["role_model", "-not_role_model"],
  "combined_admirability": [
    "role_model",
    "-not_role_model",
    "pos_gender_rep",
    "pos_ethnic_rep"
  ],
  "identification": ["similarity", "ethnic_match", "ethnic_familiarity"]
}

construct_list = [
  "attractiveness",
  "youth",
  "sexualization",
  "muscles",
  "thinness",
  "body_realism",
  "clothing_realism",
  "combined_realism",
  "attire_sexualization",
  "combined_sexualization",
  "combined_ethnic_signals",
  "positive_gender_rep",
  "positive_ethnic_rep",
  "admirability",
  "combined_admirability",
]

pers_construct_list = [
  "identification"
]

def extract_construct(row, construct):
  # TODO
  components = constructs[construct]
  return combine_values(row, *components)
 
enfreakment_types = [
  "supermodel",
  "brute",
  "ethnic",
  "unmartial",
  "villain"
]

enfreakments = {
  "supermodel": (
    lambda row: combine_values(
      row,
      "attractiveness",
      "sexualization",
      "attire_sexualization",
      "thinness",
      "youth",
    )
  ),
  "brute": (
    lambda row: combine_values(
      row,
      "-attractiveness",
      "-sexualization",
      "-attire_sexualization",
      "-thinness",
      "muscles",
      "-positive_gender_rep",
      "-positive_ethnic_rep",
      "-admirability"
    )
  ),
  "ethnic": (
    lambda row: combine_values(
      row,
      "combined_ethnic_signals",
      "-positive_ethnic_rep",
    )
  ),
  "unmartial": (
    lambda row: combine_values(
      row,
      "-muscles",
      "-thinness",
      "-youth"
    )
  ),
  "villain": (
    lambda row: combine_values(
      row,
      "-positive_gender_rep",
      "-positive_ethnic_rep",
      "-admirability",
    )
  ),
}

def combine_values(row, *constructs):
  sum = 0
  n = 0
  for c in constructs:
    if c[0] == '-':
      key = c[1:]
    else:
      key = c
    val = nv(row[key])
    if val == None:
      continue
    n += 1
    if c[0] == '-':
      sum += 8 - val
    else:
      sum += val

  if n > 0:
    return sum / n
  else:
    return None

char_prop_untangle = {
  "game": "game",
  "id": "id",
  "species": "species",
  "gender": "gender",
  "name": "name",
  "shortname": "shortname",
  "possessive": "possessive",
  "origin": "origin",
  "origingroup": "origingroup",
  "country": "country",
  "flag": "flag",
  "alt_country": "alt_country",
  "alt_flag": "alt_flag",
  "height": "height",
  "weight": "weight",
  "occupation": "occupation",
  "bio": "bio",
  "quote": "quote",
}

skin_tones = {
  "abigail": "fair",
  "akuma": "dark",
  "akumat7": "dark",
  "alex": "fair",
  "alisa": "fair",
  "asuka": "fair",
  "balrog": "dark",
  "birdie": "dark",
  "bob": "fair",
  "bryan": "fair",
  "cammy": "fair",
  "chun_li": "fair",
  "claudio": "fair",
  "deviljin": "fair",
  "dhalsim": "dark",
  "dragunov": "fair",
  "ed": "fair",
  "eddy": "dark",
  "f_a_n_g": "fair",
  "feng": "fair",
  "guile": "fair",
  "heihachi": "fair",
  "hwoarang": "fair",
  "ibuki": "fair",
  "jack7": "fair",
  "jin": "fair",
  "josie": "fair",
  "juri": "fair",
  "karin": "fair",
  "katarina": "fair",
  "kazumi": "fair",
  "kazuya": "fair",
  "ken": "fair",
  "king": "fair",
  "kolin": "fair",
  "lars": "fair",
  "laura": "dark",
  "law": "fair",
  "lee": "fair",
  "leo": "fair",
  "lili": "fair",
  "luckychloe": "fair",
  "m_bison": "fair",
  "menat": "dark",
  "miguel": "dark",
  "nash": "fair",
  "necalli": "dark",
  "nina": "fair",
  "paul": "fair",
  "r_mika": "fair",
  "r_mika": "fair",
  "rashid": "fair",
  "raven": "dark",
  "ryu": "fair",
  "shaheen": "fair",
  "steve": "fair",
  "urien": "dark",
  "vega": "fair",
  "xiaoyu": "fair",
  "zangief": "fair",
  "zeku": "fair"
}

alt_skin_tones = {
  "ryu": "fair",
  "chun_li": "fair",
  "nash": "fair",
  "m_bison": "fair",
  "cammy": "fair",
  "birdie": "fair",
  "ken": "fair",
  "necalli": "dark",
  "vega": "fair",
  "r_mika": "fair",
  "rashid": "dark",
  "karin": "fair",
  "zangief": "fair",
  "laura": "dark",
  "dhalsim": "dark",
  "f_a_n_g": "fair",
  "alex": "fair",
  "guile": "fair",
  "ibuki": "fair",
  "balrog": "dark",
  "juri": "fair",
  "urien": "dark",
  "akuma": "dark",
  "kolin": "fair",
  "ed": "fair",
  "abigail": "fair",
  "menat": "dark",
  "zeku": "dark",
  "akumat7": "dark",
  "alisa": "fair",
  "asuka": "fair",
  "bob": "fair",
  "bryan": "dark",
  "claudio": "fair",
  "deviljin": "dark",
  "dragunov": "fair",
  "eddy": "dark",
  "eliza": "fair",
  "feng": "fair",
  "gigas": "fair",
  "heihachi": "fair",
  "hwoarang": "fair",
  "jack7": "fair",
  "jin": "fair",
  "josie": "dark",
  "katarina": "dark",
  "kazumi": "fair",
  "kazuya": "dark",
  "king": "dark",
  "kuma": "dark",
  "lars": "fair",
  "law": "fair",
  "lee": "fair",
  "leo": "fair",
  "lili": "fair",
  "luckychloe": "fair",
  "miguel": "dark",
  "nina": "fair",
  "panda": "fair",
  "paul": "fair",
  "raven": "dark",
  "shaheen": "dark",
  "steve": "fair",
  "xiaoyu": "fair",
  "yoshimitsu": "fair",
}

def construct_aliases():
  # TODO: HERE
  return {
    ".constructs:0": "C:attractiveness",
    ".constructs:1": "C:youth",
    ".constructs:2": "C:sexualization",
    ".constructs:3": "C:muscles",
    ".constructs:4": "C:thinness",
    ".constructs:5": "C:body_realism",
    ".constructs:6": "C:clothing_realism",
    ".constructs:7": "C:combined_realism",
    ".constructs:8": "C:attire_sexualization",
    ".constructs:9": "C:combined_sexualization",
    ".constructs:10": "C:combined_ethnic_signals",
    ".constructs:11": "C:positive_gender_rep",
    ".constructs:12": "C:positive_ethnic_rep",
    ".constructs:13": "C:admirability",
    ".constructs:14": "C:combined_admirability",
  }

def nv(x):
  try:
    result = float(x)
  except:
    return None
  return result

primary_market_countries = [
  # TODO
]

secondary_market_countries = [
  # TODO
]
