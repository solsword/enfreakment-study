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
 "normalized_gender",
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
      "@attractiveness",
      "@sexualization",
      "@attire_sexualization",
      "@thinness",
      "@youth",
    )
  ),
  "brute": (
    lambda row: combine_values(
      row,
      "-@attractiveness",
      "-@sexualization",
      "-@attire_sexualization",
      "-@thinness",
      "@muscles",
      "-@positive_gender_rep",
      "-@positive_ethnic_rep",
      "-@admirability"
    )
  ),
  "ethnic": (
    lambda row: combine_values(
      row,
      "@combined_ethnic_signals",
      "-@positive_ethnic_rep",
    )
  ),
  "unmartial": (
    lambda row: combine_values(
      row,
      "-@muscles",
      "-@thinness",
      "-@youth"
    )
  ),
  "villain": (
    lambda row: combine_values(
      row,
      "-@positive_gender_rep",
      "-@positive_ethnic_rep",
      "-@admirability",
    )
  ),
}

def combine_values(row, *components):
  total = 0
  n = 0
  for c in components:
    if c[0] == '-':
      key = c[1:]
    else:
      key = c
    val = nv(row[key])
    if val == None:
      continue
    n += 1
    if c[0] == '-':
      total += 8 - val
    else:
      total += val

  if n > 0:
    return total / n
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
  "abigail": "lighter",
  "akuma": "darker",
  "akumat7": "darker",
  "alex": "lighter",
  "alisa": "lighter",
  "asuka": "lighter",
  "balrog": "darker",
  "birdie": "darker",
  "bob": "lighter",
  "bryan": "lighter",
  "cammy": "lighter",
  "chun_li": "lighter",
  "claudio": "lighter",
  "deviljin": "lighter",
  "dhalsim": "darker",
  "dragunov": "lighter",
  "ed": "lighter",
  "eddy": "darker",
  "f_a_n_g": "lighter",
  "feng": "lighter",
  "guile": "lighter",
  "heihachi": "lighter",
  "hwoarang": "lighter",
  "ibuki": "lighter",
  "jack7": "lighter",
  "jin": "lighter",
  "josie": "lighter",
  "juri": "lighter",
  "karin": "lighter",
  "katarina": "lighter",
  "kazumi": "lighter",
  "kazuya": "lighter",
  "ken": "lighter",
  "king": "lighter",
  "kolin": "lighter",
  "lars": "lighter",
  "laura": "darker",
  "law": "lighter",
  "lee": "lighter",
  "leo": "lighter",
  "lili": "lighter",
  "luckychloe": "lighter",
  "m_bison": "lighter",
  "menat": "darker",
  "miguel": "darker",
  "nash": "lighter",
  "necalli": "darker",
  "nina": "lighter",
  "paul": "lighter",
  "r_mika": "lighter",
  "r_mika": "lighter",
  "rashid": "lighter",
  "raven": "darker",
  "ryu": "lighter",
  "shaheen": "lighter",
  "steve": "lighter",
  "urien": "darker",
  "vega": "lighter",
  "xiaoyu": "lighter",
  "zangief": "lighter",
  "zeku": "lighter"
}

alt_skin_tones = {
  "ryu": "lighter",
  "chun_li": "lighter",
  "nash": "lighter",
  "m_bison": "lighter",
  "cammy": "lighter",
  "birdie": "lighter",
  "ken": "lighter",
  "necalli": "darker",
  "vega": "lighter",
  "r_mika": "lighter",
  "rashid": "darker",
  "karin": "lighter",
  "zangief": "lighter",
  "laura": "darker",
  "dhalsim": "darker",
  "f_a_n_g": "lighter",
  "alex": "lighter",
  "guile": "lighter",
  "ibuki": "lighter",
  "balrog": "darker",
  "juri": "lighter",
  "urien": "darker",
  "akuma": "darker",
  "kolin": "lighter",
  "ed": "lighter",
  "abigail": "lighter",
  "menat": "darker",
  "zeku": "darker",
  "akumat7": "darker",
  "alisa": "lighter",
  "asuka": "lighter",
  "bob": "lighter",
  "bryan": "darker",
  "claudio": "lighter",
  "deviljin": "darker",
  "dragunov": "lighter",
  "eddy": "darker",
  "eliza": "lighter",
  "feng": "lighter",
  "gigas": "lighter",
  "heihachi": "lighter",
  "hwoarang": "lighter",
  "jack7": "lighter",
  "jin": "lighter",
  "josie": "darker",
  "katarina": "darker",
  "kazumi": "lighter",
  "kazuya": "darker",
  "king": "darker",
  "kuma": "darker",
  "lars": "lighter",
  "law": "lighter",
  "lee": "lighter",
  "leo": "lighter",
  "lili": "lighter",
  "luckychloe": "lighter",
  "miguel": "darker",
  "nina": "lighter",
  "panda": "lighter",
  "paul": "lighter",
  "raven": "darker",
  "shaheen": "darker",
  "steve": "lighter",
  "xiaoyu": "lighter",
  "yoshimitsu": "lighter",
}

def construct_aliases():
  """
  Creates aliases for the items that are stored as arrays:

    ratings
    personal_ratings
    med_ratings
    med_personal
    participant_personal
    constructs
    med_constructs
    pers_constructs
    med_pers_constructs
    enfreakments

  """
  result = {}
  for i, r in enumerate(ratings):
    result[".ratings:{}".format(i)] = "R:{}".format(r)
    result[".med_ratings:{}".format(i)] = "~R:{}".format(r)
  for i, r in enumerate(personal_ratings):
    result[".personal_ratings:{}".format(i)] = "PR:{}".format(r)
    result[".med_personal_ratings:{}".format(i)] = "c~PR:{}".format(r)
    result[".participant_personal:{}".format(i)] = "p~PR:{}".format(r)
  for i, c in enumerate(construct_list):
    result[".constructs:{}".format(i)] = "C:{}".format(c)
    result[".med_constructs:{}".format(i)] = "~C:{}".format(c)
  for i, pc in enumerate(pers_construct_list):
    result[".pers_constructs:{}".format(i)] = "PC:{}".format(pc)
    result[".med_pers_constructs:{}".format(i)] = "~PC:{}".format(pc)
  for i, e in enumerate(enfreakment_types):
    result[".enfreakments:{}".format(i)] = "E:{}".format(e)
  return result

def nv(x):
  try:
    result = float(x)
  except:
    return None
  return result

def reverse_aliases():
  """
  Returns the reverse mapping from construct alias names to indices in the
  constructs list.
  """
  result = {}
  aliases = construct_aliases()
  for key in aliases:
    cat, idx = key.split(':')
    prp = ':'.join(aliases[key].split(':')[1:])
    # TODO TODO
    result[cat + '.' + prp] = cat + ':' + idx
  return result
