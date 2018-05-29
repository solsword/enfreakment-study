#!/usr/bin/env python3

import sys
import json
import random

import properties

import numpy as np

from scipy.stats import ttest_ind

from krippendorff import alpha as kr_alpha

sep_chars = ".:"

ALIASES = properties.reverse_aliases()

def get(row, index):
  """
  Retrieve from  a row according to a string index.
  """
  if (index in ALIASES):
    index = ALIASES[index]
  try:
    first = ""
    i = 0
    leftovers = False
    for i, c in enumerate(index):
      if i == 0:
        continue
      if c in sep_chars:
        leftovers = True
        break
      first += c

    if leftovers:
      rest = index[i:]
    else:
      rest = ""

    try:
      first = int(first)
    except:
      pass

    if rest:
      if isinstance(row, dict):
        sub = row.get(first, None)
      else:
        sub = row[first]
      if sub != None:
        return get(sub, rest)
      else:
        return None
    else:
      if isinstance(row, dict):
        return row.get(first, None)
      else:
        return row[first]
  except TypeError:
    raise ValueError("Invalid index: '{}'".format(index))

characters = [ "ryu", "chun_li", "nash", "m_bison", "cammy", "birdie", "ken", "necalli", "vega", "r_mika", "rashid", "karin", "zangief", "laura", "dhalsim", "f_a_n_g", "alex", "guile", "ibuki", "balrog", "juri", "urien", "akuma", "kolin", "ed", "abigail", "menat", "zeku", "akumat7", "alisa", "asuka", "bob", "bryan", "claudio", "dragunov", "eddy", "feng", "heihachi", "hwoarang", "jack7", "jin", "josie", "katarina", "kazumi", "kazuya", "king", "lars", "law", "lee", "leo", "lili", "luckychloe", "miguel", "nina", "paul", "raven", "shaheen", "steve", "xiaoyu", "deviljin", ]

charmap = {
  char: i
    for i, char in enumerate(characters)
}

test_agreement = [
  ".ratings.attire_ethnicity",
  ".ratings.attire_not_sexualized",
  ".ratings.attire_sexualized",
  ".ratings.attractive",
  ".ratings.chubby",
  ".ratings.costume",
  ".ratings.ethnic_stereotypes",
  ".ratings.exaggerated_body",
  ".ratings.gender_stereotypes",
  ".ratings.muscular",
  ".ratings.non_muscular",
  ".ratings.not_role_model",
  ".ratings.not_sexualized",
  ".ratings.obv_ethnicity",
  ".ratings.old",
  ".ratings.pos_ethnic_rep",
  ".ratings.pos_gender_rep",
  ".ratings.realistic_body",
  ".ratings.realistic_clothing",
  ".ratings.role_model",
  ".ratings.sexualized",
  ".ratings.skinny",
  ".ratings.ugly",
  ".ratings.young",
]

def is_japanese(row):
  return get(row, ".character.country") == "Japan"

def is_majority(row):
  return get(row, ".character.is_token") == "Majority"

def is_minority(row):
  return get(row, ".character.is_token") == "Minority"

def is_token(row):
  return get(row, ".character.is_token") == "Token"

def character_female(row):
  return get(row, ".character.gendergroup") == "women"

def character_male(row):
  return get(row, ".character.gendergroup") == "men"

def participant_female(row):
  return get(row, ".participant.gender_description") == "Female"

def infrequent_player(row):
  return get(row, ".participant.play_frequency") in ("never", "infrequent")

def is_fair_skinned(row):
  return get(row, ".character.skin_tone") == "fair"

def is_dark_skinned(row):
  return get(row, ".character.skin_tone") == "dark"

# monthly players aren't in either group

def frequent_player(row):
  return get(row, ".participant.play_frequency") in ("daily", "weekly")

original_hypotheses = [
  ("Japanese:more-realistic", ".constructs.body_realism", is_japanese, None, "+"),
  ("Women:less-muscular", ".constructs.muscles", character_female, None, "-"),
  ("Japanese:thinner", ".constructs.thinness", is_japanese, None, "+"),
  ("Women:thinner", ".constructs.thinness", character_female, None, "+"),

  ("Women:younger", ".constructs.youth", character_female, None, "+"),

  ("Women:more-attractive", ".constructs.attractiveness", character_female, None, "+"),
  ("Japanese:more-attractive", ".constructs.attractiveness", is_japanese, None, "+"),
  ("Majority:more-attractive", ".constructs.attractiveness", is_majority, None, "+"),
  ("Token:less-attractive", ".constructs.attractiveness", is_token, None, "-"),

  ("Women:more-sexualized", ".constructs.sexualization", character_female, None,"+"),
  ("Women:more-attire-sexualized", ".constructs.attire_sexualization", character_female, None,"+"),

  ("Women:less-realistic-clothes", ".constructs.clothing_realism", character_female, None, "-"),
  ("Japanese:more-realistic-clothes", ".constructs.clothing_realism", is_japanese, None, "+"),
  ("Majority:more-realistic-clothes", ".constructs.clothing_realism", is_majority, None, "+"),
  ("Token:less-realistic-clothes", ".constructs.clothing_realism", is_token, None, "-"),

  ("Women:more-obvious-ethnicity", ".constructs.combined_ethnic_signals", character_female, None,"+"),
  ("Japanese:less-obvious-ethnicity", ".constructs.combined_ethnic_signals", is_japanese, None, "-"),
  ("Majority:less-obvious-ethnicity", ".constructs.combined_ethnic_signals", is_majority, None,"-"),
  ("Token:more-obvious-ethnicity", ".constructs.combined_ethnic_signals", is_token, None, "+"),

  ("Women:less-admirable", ".constructs.admirableness", character_female, None, "-"),
  ("Japanese:more-admirable", ".constructs.admirableness", is_japanese, None, "+"),

  ("Women:less-positive-gender", ".constructs.positive_gender_rep", character_female, None, "-"),

  ("Japanese:more-positive-ethnicity", ".constructs.positive_ethnic_rep", is_japanese, None, "+"),
  ("Majority:more-positive-ethnicity", ".constructs.positive_ethnic_rep", is_majority, None, "+"),
  ("Token:less-positive-ethnicity", ".constructs.positive_ethnic_rep", is_token, None, "-"),
]

def colonizer_country(row):
  return get(row, ".character.country") in (
    "Japan",
    "United States of America",
    "Canada",
    "Germany",
    "Italy",
    "Spain",
    "United Kingdom",
    "Monaco",
    "Russia",
    "Sweden",
  )

def colonized_country(row):
  return get(row, ".character.country") in (
    "Brazil",
    "China",
    "Egypt",
    "India",
    "Ireland",
    "Mexico",
    "Middle East",
    "Philippines",
    "Saudi Arabia",
    "South Korea",
  )

def unknown_country(row):
  return get(row, ".character.country") == "Unknown"

def dark_skinned_women(row):
  return character_female(row) and get(row, ".character.skin_tone") == "dark"

def fair_skinned_women(row):
  return character_female(row) and get(row, ".character.skin_tone") == "fair"

def dark_skinned_men(row):
  return not character_female(row) and get(row, ".character.skin_tone") =="dark"

def fair_skinned_men(row):
  return not character_female(row) and get(row, ".character.skin_tone") =="fair"

def colonized_women(row):
  return character_female(row) and colonized_country(row)

def colonizer_women(row):
  return character_female(row) and colonizer_country(row)

def colonized_men(row):
  return not character_female(row) and colonized_country(row)

def colonizer_men(row):
  return not character_female(row) and colonizer_country(row)

def participant_nonwhite(row):
  return get(row, ".participant.normalized_ethnicity.White") == None

def participant_white(row):
  return get(row, ".participant.normalized_ethnicity.White") == 1

novel_hypotheses = [
  # Brute sub-components:
  ("Fair:more-realistic", ".constructs.body_realism", is_fair_skinned, is_dark_skinned, "+"),
  ("Fair:more-attractive", ".constructs.attractiveness", is_fair_skinned, is_dark_skinned, "+"),
  ("Fair:less-muscular", ".constructs.muscles", is_fair_skinned, is_dark_skinned, "-"),
  ("Fair:thinner", ".constructs.thinness", is_fair_skinned, is_dark_skinned, "+"),

  ("Colonizer:more-realistic", ".constructs.body_realism", colonizer_country, colonized_country, "+"),
  ("Colonizer:more-attractive", ".constructs.attractiveness", colonizer_country, colonized_country, "+"),
  ("Colonizer:less-muscular", ".constructs.muscles", colonizer_country, colonized_country, "-"),
  ("Colonizer:thinner", ".constructs.thinness", colonizer_country, colonized_country, "+"),

  # Ethnic sub-components (minus positive_ethnic_rep):
  ("Fair:more-realistic-clothing", ".constructs.clothing_realism", is_fair_skinned, is_dark_skinned, "+"),
  ("Fair:less-obvious-ethnicity", ".constructs.combined_ethnic_signals", is_fair_skinned, is_dark_skinned, "-"),

  ("Colonizer:more-realistic-clothing", ".constructs.clothing_realism", colonizer_country, colonized_country, "+"),
  ("Colonizer:less-obvious-ethnicity", ".constructs.combined_ethnic_signals", colonizer_country, colonized_country, "-"),

  # Villain sub-components
  ("Fair:more-admirable", ".constructs.admirableness", is_fair_skinned, is_dark_skinned, "+"),
  ("Fair:more-positive-ethnicity", ".constructs.positive_ethnic_rep", is_fair_skinned, is_dark_skinned, "+"),
  ("Fair:more-positive-gender", ".constructs.positive_gender_rep", is_fair_skinned, is_dark_skinned, "+"),

  ("Colonizer:more-admirable", ".constructs.admirableness", colonizer_country, colonized_country, "+"),
  ("Colonizer:more-positive-ethnicity", ".constructs.positive_ethnic_rep", colonizer_country, colonized_country, "+"),
  ("Colonizer:more-positive-gender", ".constructs.positive_gender_rep", colonizer_country, colonized_country, "+"),

  # Participant gender/frequency vs. gender perceptions:
  ("Female-Raters:recognize-bad-gender-rep", ".constructs.positive_gender_rep", participant_female, None, "-"),
  ("Infrequent-Players:recognize-bad-gender-rep", ".constructs.positive_gender_rep", infrequent_player, None, "-"),
  ("Frequent-Players:ignore-bad-gender-rep", ".constructs.positive_gender_rep", frequent_player, None, "+"),

  # Participant ethnicity/frequency vs. ethnicity perceptions:
  ("Nonwhite-Raters:recognize-bad-ethnic-rep", ".constructs.positive_ethnic_rep", participant_nonwhite, None, "-"),
  ("White-Raters:ignore-bad-ethnic-rep", ".constructs.positive_ethnic_rep", participant_white, None, "+"),
  ("Infrequent-Players:recognize-bad-ethnic-rep", ".constructs.positive_ethnic_rep", infrequent_player, None, "-"),
  ("Frequent-Players:ignore-bad-ethnic-rep", ".constructs.positive_ethnic_rep", frequent_player, None, "+"),

  # Intersections
  ("Fair-Women:more-realistic", ".constructs.body_realism", fair_skinned_women, dark_skinned_women, "+"),
  ("Fair-Women:more-attractive", ".constructs.attractiveness", fair_skinned_women, dark_skinned_women, "+"),
  ("Fair-Women:less-sexualized", ".constructs.sexualization", fair_skinned_women, dark_skinned_women, "-"),
  ("Fair-Women:less-attire-sexualized", ".constructs.attire_sexualization", fair_skinned_women, dark_skinned_women, "-"),
  ("Fair-Women:less-muscular", ".constructs.muscles", fair_skinned_women, dark_skinned_women, "-"),
  ("Fair-Women:thinner", ".constructs.thinness", fair_skinned_women, dark_skinned_women, "+"),
  ("Fair-Women:older", ".constructs.youth", fair_skinned_women, dark_skinned_women, "-"),
  ("Fair-Women:more-admirable", ".constructs.admirableness", fair_skinned_women, dark_skinned_women, "+"),
  ("Fair-Women:more-positive-gender", ".constructs.positive_gender_rep", fair_skinned_women, dark_skinned_women, "+"),
  ("Fair-Women:more-positive-ethnic", ".constructs.positive_ethnic_rep", fair_skinned_women, dark_skinned_women, "+"),

  ("Colonizer-Women:more-realistic", ".constructs.body_realism", colonizer_women, colonized_women, "+"),
  ("Colonizer-Women:more-attractive", ".constructs.attractiveness", colonizer_women, colonized_women, "+"),
  ("Colonizer-Women:less-sexualized", ".constructs.sexualization", colonizer_women, colonized_women, "-"),
  ("Colonizer-Women:less-attire-sexualized", ".constructs.attire_sexualization", colonizer_women, colonized_women, "-"),
  ("Colonizer-Women:less-muscular", ".constructs.muscles", colonizer_women, colonized_women, "-"),
  ("Colonizer-Women:thinner", ".constructs.thinness", colonizer_women, colonized_women, "+"),
  ("Colonizer-Women:older", ".constructs.youth", colonizer_women, colonized_women, "-"),
  ("Colonizer-Women:more-admirable", ".constructs.admirableness", colonizer_women, colonized_women, "+"),
  ("Colonizer-Women:more-positive-gender", ".constructs.positive_gender_rep", colonizer_women, colonized_women, "+"),
  ("Colonizer-Women:more-positive-ethnic", ".constructs.positive_ethnic_rep", colonizer_women, colonized_women, "+"),

  ("Fair-Men:more-realistic", ".constructs.body_realism", fair_skinned_men, dark_skinned_men, "+"),
  ("Fair-Men:more-attractive", ".constructs.attractiveness", fair_skinned_men, dark_skinned_men, "+"),
  ("Fair-Men:less-muscular", ".constructs.muscles", fair_skinned_men, dark_skinned_men, "-"),
  ("Fair-Men:thinner", ".constructs.thinness", fair_skinned_men, dark_skinned_men, "+"),
  ("Fair-Men:older", ".constructs.youth", fair_skinned_men, dark_skinned_men, "-"),
  ("Fair-Men:more-admirable", ".constructs.admirableness", fair_skinned_men, dark_skinned_men, "+"),
  ("Fair-Men:more-positive-gender", ".constructs.positive_gender_rep", fair_skinned_men, dark_skinned_men, "+"),
  ("Fair-Men:more-positive-ethnic", ".constructs.positive_ethnic_rep", fair_skinned_men, dark_skinned_men, "+"),

  ("Colonizer-Men:more-realistic", ".constructs.body_realism", colonizer_men, colonized_men, "+"),
  ("Colonizer-Men:more-attractive", ".constructs.attractiveness", colonizer_men, colonized_men, "+"),
  ("Colonizer-Men:less-muscular", ".constructs.muscles", colonizer_men, colonized_men, "-"),
  ("Colonizer-Men:thinner", ".constructs.thinness", colonizer_men, colonized_men, "+"),
  ("Colonizer-Men:older", ".constructs.youth", colonizer_men, colonized_men, "-"),
  ("Colonizer-Men:more-admirable", ".constructs.admirableness", colonizer_men, colonized_men, "+"),
  ("Colonizer-Men:more-positive-gender", ".constructs.positive_gender_rep", colonizer_men, colonized_men, "+"),
  ("Colonizer-Men:more-positive-ethnic", ".constructs.positive_ethnic_rep", colonizer_men, colonized_men, "+"),

  # Unknown dumping?
  ("Unknown:less-realistic", ".constructs.body_realism", unknown_country, None, "-"),
  ("Unknown:more-muscular", ".constructs.muscles", unknown_country, None, "+"),
  ("Unknown:less-attractive", ".constructs.attractiveness", unknown_country, None, "-"),
  ("Unknown:fatter", ".constructs.thinness", unknown_country, None, "-"),
  ("Unknown:older", ".constructs.youth", unknown_country, None, "-"),
  ("Unknown:less-admirable", ".constructs.admirableness", unknown_country, None, "-"),
  ("Unknown:worse-gender-rep", ".constructs.positive_gender_rep", unknown_country, None, "-"),
  ("Unknown:worse-ethnic-rep", ".constructs.positive_ethnic_rep", unknown_country, None, "-"),
]

framedata_hypotheses = [
  # Men are bulkier
  ("Health:men-healthier", ".character.stats.health", character_male, character_female, '+'),
  ("Health:men-higher-stun", ".character.stats.stun", character_male, character_female, '+'),
  ("Size:men-grab-farther", ".character.stats.throw_range", character_male, character_female, '+'),
  # Women are more agile
  ("Agility:women-jump-higher", ".character.stats.jump_height", character_female, character_male, '+'),
  ("Agility:women-jump-farther", ".character.stats.jump_distance", character_female, character_male, '+'),
  ("Agility:women-dash-farther", ".character.stats.dash_distance", character_female, character_male, '+'),
  ("Agility:women-faster", ".character.stats.speed", character_female, character_male, '+'),
  # Men hit harder & slower
  ("Normals:men-more-damage", ".character.stats.normals.avg_hit_damage", character_male, character_female, '+'),
  ("Attacks:men-more-damage", ".character.stats.all_moves.avg_hit_damage", character_male, character_female, '+'),
  ("Normals:men-more-stun", ".character.stats.normals.avg_hit_stun", character_male, character_female, '+'),
  ("Attacks:men-more-stun", ".character.stats.all_moves.avg_hit_stun", character_male, character_female, '+'),
  ("Normals:men-active-longer", ".character.stats.normals.avg_active_frames", character_male, character_female, '+'),
  ("Attacks:men-active-longer", ".character.stats.all_moves.avg_active_frames", character_male, character_female, '+'),
  ("Normals:women-hit-more", ".character.stats.normals.avg_hit_count", character_female, character_male, '+'),
  ("Attacks:women-hit-more", ".character.stats.all_moves.avg_hit_count", character_female, character_male, '+'),
  ("Normals:men-slower", ".character.stats.normals.avg_frames_per_hit", character_male, character_female, '+'),
  ("Attacks:men-slower", ".character.stats.all_moves.avg_frames_per_hit", character_male, character_female, '+'),
  ("Normals:men-more-delayed", ".character.stats.normals.avg_dead_frames", character_male, character_female, '+'),
  ("Attacks:men-more-delayed", ".character.stats.all_moves.avg_dead_frames", character_male, character_female, '+'),
  ("Normals:women-plus-on-hit", ".character.stats.normals.avg_hit_advantage", character_female, character_male, '+'),
  ("Attacks:women-plus-on-hit", ".character.stats.all_moves.avg_hit_advantage", character_female, character_male, '+'),
  ("Normals:women-plus-on-block", ".character.stats.normals.avg_block_advantage", character_female, character_male, '+'),
  ("Attacks:women-plus-on-block", ".character.stats.all_moves.avg_block_advantage", character_female, character_male, '+'),
  ("Normals:women-more-multihit", ".character.stats.normals.multihit_proportion", character_female, character_male, '+'),
  ("Attacks:women-more-multihit", ".character.stats.all_moves.multihit_proportion", character_female, character_male, '+'),
  ("Normals:women-more-combos", ".character.stats.normals.combo_proportion", character_female, character_male, '+'),
  ("Attacks:women-more-combos", ".character.stats.all_moves.combo_proportion", character_female, character_male, '+'),
  ("Normals:men-more-knockdowns", ".character.stats.normals.knockdown_proportion", character_male, character_female, '+'),
  ("Attacks:men-more-knockdowns", ".character.stats.all_moves.knockdown_proportion", character_male, character_female, '+'),
  # Men have safer attacks
  ("Normals:men-safer", ".character.stats.normals.unsafe_proportion", character_female, character_male, '+'),
  ("Attacks:men-safer", ".character.stats.all_moves.unsafe_proportion", character_female, character_male, '+'),
  # Dark-skinned characters are bulkier
  ("Health:dark-men-healthier", ".character.stats.health", dark_skinned_men, fair_skinned_men, '+'),
  ("Health:dark-men-higher-stun", ".character.stats.stun", dark_skinned_men, fair_skinned_men, '+'),
  ("Size:dark-men-grab-farther", ".character.stats.throw_range", dark_skinned_men, fair_skinned_men, '+'),
  # Fair-skinned characters are faster
  ("Agility:fair-men-faster", ".character.stats.speed", fair_skinned_men, dark_skinned_men, '+'),
  # Dark-skinned characters hit harder/slower
  ("Normals:dark-men-more-damage", ".character.stats.normals.avg_hit_damage", dark_skinned_men, fair_skinned_men, '+'),
  ("Attacks:dark-men-more-damage", ".character.stats.all_moves.avg_hit_damage", dark_skinned_men, fair_skinned_men, '+'),
  ("Normals:dark-men-more-stun", ".character.stats.normals.avg_hit_stun", dark_skinned_men, fair_skinned_men, '+'),
  ("Attacks:dark-men-more-stun", ".character.stats.all_moves.avg_hit_stun", dark_skinned_men, fair_skinned_men, '+'),
  ("Normals:dark-men-active-longer", ".character.stats.normals.avg_active_frames", dark_skinned_men, fair_skinned_men, '+'),
  ("Attacks:dark-men-active-longer", ".character.stats.all_moves.avg_active_frames", dark_skinned_men, fair_skinned_men, '+'),
  ("Normals:fair-men-hit-more", ".character.stats.normals.avg_hit_count", fair_skinned_men, dark_skinned_men, '+'),
  ("Attacks:fair-men-hit-more", ".character.stats.all_moves.avg_hit_count", fair_skinned_men, dark_skinned_men, '+'),
  ("Normals:dark-men-slower", ".character.stats.normals.avg_frames_per_hit", dark_skinned_men, fair_skinned_men, '+'),
  ("Attacks:dark-men-slower", ".character.stats.all_moves.avg_frames_per_hit", dark_skinned_men, fair_skinned_men, '+'),
  ("Normals:dark-men-more-delayed", ".character.stats.normals.avg_dead_frames", dark_skinned_men, fair_skinned_men, '+'),
  ("Attacks:dark-men-more-delayed", ".character.stats.all_moves.avg_dead_frames", dark_skinned_men, fair_skinned_men, '+'),
  ("Normals:fair-men-plus-on-hit", ".character.stats.normals.avg_hit_advantage", fair_skinned_men, dark_skinned_men, '+'),
  ("Attacks:fair-men-plus-on-hit", ".character.stats.all_moves.avg_hit_advantage", fair_skinned_men, dark_skinned_men, '+'),
  ("Normals:fair-men-plus-on-block", ".character.stats.normals.avg_block_advantage", fair_skinned_men, dark_skinned_men, '+'),
  ("Attacks:fair-men-plus-on-block", ".character.stats.all_moves.avg_block_advantage", fair_skinned_men, dark_skinned_men, '+'),
  ("Normals:fair-men-more-multihit", ".character.stats.normals.multihit_proportion", fair_skinned_men, dark_skinned_men, '+'),
  ("Attacks:fair-men-more-multihit", ".character.stats.all_moves.multihit_proportion", fair_skinned_men, dark_skinned_men, '+'),
  ("Normals:fair-men-more-combos", ".character.stats.normals.combo_proportion", fair_skinned_men, dark_skinned_men, '+'),
  ("Attacks:fair-men-more-combos", ".character.stats.all_moves.combo_proportion", fair_skinned_men, dark_skinned_men, '+'),
  ("Normals:dark-men-more-knockdowns", ".character.stats.normals.knockdown_proportion", dark_skinned_men, fair_skinned_men, '+'),
  ("Attacks:dark-men-more-knockdowns", ".character.stats.all_moves.knockdown_proportion", dark_skinned_men, fair_skinned_men, '+'),
]

all_hypotheses = original_hypotheses + novel_hypotheses + framedata_hypotheses

hgroups = {
  "Women sexualized": [
    "Women:less-muscular",
    "Women:younger",
    "Women:thinner",
    "Women:more-attractive",
    "Women:more-sexualized",
    "Women:more-attire-sexualized",
  ],
  "Women ethnicity exaggerated": [
    "Women:less-realistic-clothes",
    "Women:more-obvious-ethnicity",
  ],
  "Women disliked": [
    "Women:less-admirable",
    "Women:less-positive-gender",
  ],
  "Japanese preferred": [
    "Japanese:more-realistic",
    "Japanese:thinner",
    "Japanese:more-attractive",
    "Japanese:more-admirable",
    "Japanese:more-positive-ethnicity",
  ],
  "Japanese more realistic": [
    "Japanese:more-realistic-clothes",
    "Japanese:less-obvious-ethnicity",
  ],
  "Majority preferred/realistic": [
    "Majority:more-attractive",
    "Majority:more-realistic-clothes",
    "Majority:less-obvious-ethnicity",
    "Majority:more-positive-ethnicity",
  ],
  "Token suppressed/unrealistic": [
    "Token:less-attractive",
    "Token:less-realistic-clothes",
    "Token:more-obvious-ethnicity",
    "Token:less-positive-ethnicity",
  ],
  "Fair-skinned less brutish": [
    "Fair:more-realistic",
    "Fair:more-attractive",
    "Fair:less-muscular",
    "Fair:thinner",
  ],
  "Colonizer less brutish": [
    "Colonizer:more-realistic",
    "Colonizer:more-attractive",
    "Colonizer:less-muscular",
    "Colonizer:thinner",
  ],
  "Fair-skinned less exaggerated": [
    "Fair:more-realistic-clothing",
    "Fair:less-obvious-ethnicity",
  ],
  "Colonizer less exaggerated": [
    "Colonizer:more-realistic-clothing",
    "Colonizer:less-obvious-ethnicity",
  ],
  "Fair-skinned less villainous": [
    "Fair:more-admirable",
    "Fair:more-positive-ethnicity",
    "Fair:more-positive-gender",
  ],
  "Colonizer less villainous": [
    "Colonizer:more-admirable",
    "Colonizer:more-positive-ethnicity",
    "Colonizer:more-positive-gender",
  ],
  "Women and non-gamers more aware of gender stereotypes": [
    "Female-Raters:recognize-bad-gender-rep",
    "Infrequent-Players:recognize-bad-gender-rep",
    "Frequent-Players:ignore-bad-gender-rep",
  ],
  "Nonwhite and non-gamers more aware of racial stereotypes": [
    "Nonwhite-Raters:recognize-bad-ethnic-rep",
    "White-Raters:ignore-bad-ethnic-rep",
    "Infrequent-Players:recognize-bad-ethnic-rep",
    "Frequent-Players:ignore-bad-ethnic-rep",
  ],
  "Fair-skinned women more attractive/less sexualized then dark-skinned women":[
    "Fair-Women:more-realistic",
    "Fair-Women:more-attractive",
    "Fair-Women:less-sexualized",
    "Fair-Women:less-attire-sexualized",
    "Fair-Women:less-muscular",
    "Fair-Women:thinner",
    "Fair-Women:older",
    "Fair-Women:more-admirable",
    "Fair-Women:more-positive-gender",
    "Fair-Women:more-positive-ethnic",
  ],
  "Colonizer women more attractive/less sexualized than colonized women": [
    "Colonizer-Women:more-realistic",
    "Colonizer-Women:more-attractive",
    "Colonizer-Women:less-sexualized",
    "Colonizer-Women:less-attire-sexualized",
    "Colonizer-Women:less-muscular",
    "Colonizer-Women:thinner",
    "Colonizer-Women:older",
    "Colonizer-Women:more-admirable",
    "Colonizer-Women:more-positive-gender",
    "Colonizer-Women:more-positive-ethnic",
  ],
  "Fair-skinned men less brutish than dark-skinned men": [
    "Fair-Men:more-realistic",
    "Fair-Men:more-attractive",
    "Fair-Men:less-muscular",
    "Fair-Men:thinner",
    "Fair-Men:older",
    "Fair-Men:more-admirable",
    "Fair-Men:more-positive-gender",
    "Fair-Men:more-positive-ethnic",
  ],
  "Colonizer men less brutish than colonized men": [
    "Colonizer-Men:more-realistic",
    "Colonizer-Men:more-attractive",
    "Colonizer-Men:less-muscular",
    "Colonizer-Men:thinner",
    "Colonizer-Men:older",
    "Colonizer-Men:more-admirable",
    "Colonizer-Men:more-positive-gender",
    "Colonizer-Men:more-positive-ethnic",
  ],
  "Unknown country used for villains/brutes": [
    "Unknown:less-realistic",
    "Unknown:more-muscular",
    "Unknown:less-attractive",
    "Unknown:fatter",
    "Unknown:older",
    "Unknown:less-admirable",
    "Unknown:worse-gender-rep",
    "Unknown:worse-ethnic-rep",
  ],
  "Men are bulkier": [
    "Health:men-healthier",
    "Health:men-higher-stun",
    "Size:men-grab-farther",
  ],
  "Women are more agile": [
    "Agility:women-jump-higher",
    "Agility:women-jump-farther",
    "Agility:women-dash-farther",
    "Agility:women-faster",
  ],
  "Men have slower/stronger normals": [
    "Normals:men-more-damage",
    "Normals:men-more-stun",
    "Normals:men-active-longer",
    "Normals:women-hit-more",
    "Normals:men-slower",
    "Normals:men-more-delayed",
    "Normals:women-plus-on-hit",
    "Normals:women-plus-on-block",
    "Normals:women-more-multihit",
    "Normals:women-more-combos",
    "Normals:men-more-knockdowns",
    "Normals:men-safer",
  ],
  "Men have slower/stronger attacks": [
    "Attacks:men-more-damage",
    "Attacks:men-more-stun",
    "Attacks:men-active-longer",
    "Attacks:women-hit-more",
    "Attacks:men-slower",
    "Attacks:men-more-delayed",
    "Attacks:women-plus-on-hit",
    "Attacks:women-plus-on-block",
    "Attacks:women-more-multihit",
    "Attacks:women-more-combos",
    "Attacks:men-more-knockdowns",
    "Attacks:men-safer",
  ],
  "Darker-skinned men are bulkier": [
    "Health:dark-men-healthier",
    "Health:dark-men-higher-stun",
    "Size:dark-men-grab-farther",
  ],
  "Darker-skinned men are less agile": [
    "Agility:fair-men-faster",
  ],
  "Darker-skinned men have slower/stronger normals": [
    "Normals:dark-men-more-damage",
    "Normals:dark-men-more-stun",
    "Normals:dark-men-active-longer",
    "Normals:fair-men-hit-more",
    "Normals:dark-men-slower",
    "Normals:dark-men-more-delayed",
    "Normals:fair-men-plus-on-hit",
    "Normals:fair-men-plus-on-block",
    "Normals:fair-men-more-multihit",
    "Normals:fair-men-more-combos",
    "Normals:dark-men-more-knockdowns",
  ],
  "Darker-skinned men have slower/stronger attacks": [
    "Attacks:dark-men-more-damage",
    "Attacks:dark-men-more-stun",
    "Attacks:dark-men-active-longer",
    "Attacks:fair-men-hit-more",
    "Attacks:dark-men-slower",
    "Attacks:dark-men-more-delayed",
    "Attacks:fair-men-plus-on-hit",
    "Attacks:fair-men-plus-on-block",
    "Attacks:fair-men-more-multihit",
    "Attacks:fair-men-more-combos",
    "Attacks:dark-men-more-knockdowns",
  ],
}

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

  print('='*80)
  print("Starting statistical analysis...")
  print('-'*80)
  # TODO: Switch this?
  #use = t_test
  use = bootstrap_test
  print(
    "Testing {} hypotheses using {}...".format(
      len(all_hypotheses),
      use.__name__
    )
  )
  tests = init_tests(rows, all_hypotheses, use)
  print()
  effects, expected = analyze_tests(rows, tests)
  summarize_tests(effects, expected, hgroups)
  print('-'*80)
  analyze_agreement(rows)
  print('-'*80)
  print("...analysis complete.")
  print('='*80)

def bootstrap_test(
  rows,
  index,
  pos_filter,
  alt_filter=None,
  trials=15000,
  seed=1081230891
):
  pos_mean = 0
  pos_count = 0
  alt_mean = 0
  alt_count = 0
  vals = []
  hits = []
  alts = []
  nones = 0
  for i, row in enumerate(rows):
    val = get(row, index)
    if val == None:
      nones += 1
      continue
    vals.append(val)
    if pos_filter(row):
      hits.append(i - nones)
      pos_mean += val
      pos_count += 1
    elif alt_filter == None:
      alts.append(i - nones)
      alt_mean += val
      alt_count += 1

    if alt_filter != None and alt_filter(row):
      alts.append(i - nones)
      alt_mean += val
      alt_count += 1

  pos_mean /= pos_count
  alt_mean /= alt_count

  md = pos_mean - alt_mean

  random.seed(seed)
  as_diff = 0
  for t in range(trials):
    random.shuffle(vals)
    pos_mean = 0
    alt_mean = 0
    for i in hits:
      pos_mean += vals[i]
    for i in alts:
      alt_mean += vals[i]
    pos_mean /= pos_count
    alt_mean /= alt_count
    tmd = pos_mean - alt_mean
    if (md > 0 and tmd >= md) or (md < 0 and tmd <= md):
      as_diff += 1

  return md, as_diff / trials

def t_test(
  rows,
  index,
  pos_filter,
  alt_filter=None
):
  ingroup = []
  outgroup = []
  for row in rows:
    if pos_filter(row):
      val = get(row, index)
      if val != None:
        ingroup.append(val)
    elif alt_filter == None:
      val = get(row, index)
      if val != None:
        outgroup.append(val)

    if alt_filter != None and alt_filter(row):
      val = get(row, index)
      if val != None:
        outgroup.append(val)

  inmean = np.mean(ingroup)
  outmean = np.mean(outgroup)

  stat, p = ttest_ind(ingroup, outgroup, equal_var=False)

  return inmean - outmean, p

def init_tests(rows, hypotheses, method=bootstrap_test):
  """
  Constructs a bunch of test objects and returns a list of them for
  analyze_tests to process.
  """
  tests = []
  for i, (name, index, pos_filter, alt_filter, direction) in enumerate(
    hypotheses
  ):
    md, p = method(rows, index, pos_filter, alt_filter)
    print("{}/{} done...".format(i, len(hypotheses)), end="\r")
    sys.stdout.flush()

    dword = {
      "+": "greater",
      "-": "less"
    }[direction]

    cond_name = pos_filter.__name__

    if direction == "+":
      smsg = "== {} is greater for {}: {:+.3g}, p = {:.3g}".format(
        index[12:],
        cond_name,
        md,
        p
      )
      fmsg = "-- {} is indistinguishable for {}: p = {:.3g}".format(
        index[12:],
        cond_name,
        p
      )
      qmsg = "!! {} is unexpectedly smaller for {}: {:+.3g}, p = {:.3g}".format(
        index[12:],
        cond_name,
        md,
        p
      )
      qfmsg = "-- {} is indistinguishable (& unexpectedly smaller) for {}: p = {:.3g}".format(
        index[12:],
        cond_name,
        p
      )
      if md > 0:
        tests.append([name, True, md, p, smsg, fmsg])
      else:
        tests.append([name, False, md, p, qmsg, qfmsg])
    elif direction == "-":
      smsg = "== {} is smaller for {}: {:+.3g}, p = {:.3g}".format(
        index[12:],
        cond_name,
        md,
        p
      )
      fmsg = "-- {} is indistinguishable for {}: p = {:.3g}".format(
        index[12:],
        cond_name,
        p
      )
      qmsg = "!! {} is unexpectedly greater for {}: {:+.3g}, p = {:.3g}".format(
        index[12:],
        cond_name,
        md,
        p
      )
      qfmsg = "-- {} is indistinguishable (& unexpectedly greater) for {}: p = {:.3g}".format(
        index[12:],
        cond_name,
        p
      )
      if md < 0:
        tests.append([name, True, md, p, smsg, fmsg])
      else:
        tests.append([name, False, md, p, qmsg, qfmsg])
    else:
      raise ValueError("Invalid test direction: '{}'".format(direction))
  print("{}/{} done...".format(len(hypotheses), len(hypotheses)))
  return tests

def analyze_tests(rows, tests, threshold = 0.05):
  """
  Given a bunch of test objects, analyzes them and prints out results.
  """
  failed = False
  m = len(tests)
  effects = {}
  expected = {}
  for i, (name, expd, md, p, smsg, fmsg) in enumerate(
    sorted(tests, key=lambda x: x[3])
  ):
    k = i + 1
    #th = threshold / (m - i) ## Holm-Bonferroni
    th = threshold * (k/m) # Benjamini-Hochberg
    close = p < threshold
    expected[name] = expd
    if failed:
      effects[name] = None
      print("{} {} ~ {:.3g}".format(" *"[close], fmsg, th))
    elif p > th:
      effects[name] = None
      failed = True
      print("{} {} > {:.3g}".format(" *"[close], fmsg, th))
    else:
      effects[name] = md
      print("{} {} < {:.3g}".format(" *"[close], smsg, th))

  return effects, expected

def summarize_tests(effects, expected, hgroups):
  for name in hgroups:
    hypotheses = hgroups[name]
    print(name)
    for hyp in hypotheses:
      print(
        "  {} {}: {}".format(
          ' ' if expected[hyp] else '!',
          hyp,
          "{:+.3g}".format(effects[hyp]) if effects[hyp] != None else '?'
        )
      )

def analyze_agreement(rows):
  n_raters = len(rows)//5
  n_characters = len(rows)//7
  print("Rating agreement (full/categorical):")
  for t in test_agreement:
    ratings = np.full((n_raters, n_characters), np.nan)
    bin_ratings = np.full((n_raters, n_characters), np.nan)
    for row in rows:
      pid = int(get(row, ".participant.id")) - 1
      ch = get(row, ".character.id")
      cid = charmap[ch]
      if not np.isnan(ratings[pid, cid]):
        print(
          "Double-fill: [{}, {}] was {} ? {}!".format(
            pid,
            ch,
            ratings[pid, cid],
            np.isnan(ratings[pid, cid])
          ),
          file=sys.stderr
        )
        print(row, file=sys.stderr)
      val = get(row, t)
      ratings[pid,cid] = val
      bin_ratings[pid,cid] = [-1,0,1][(val>3) + (val>4)] if val else None
    # DEBUG:
    """
    if "muscular" in t:
      rgrouped = {i: [] for i in range(len(characters))}
      bingrouped = {i: { -1: 0, 0: 0, 1: 0 } for i in range(len(characters))}
      for pid in range(ratings.shape[0]):
        for cid in range(ratings.shape[1]):
          if not np.isnan(ratings[pid,cid]):
            rgrouped[cid].append(ratings[pid,cid])
          if not np.isnan(bin_ratings[pid,cid]):
            bingrouped[cid][bin_ratings[pid,cid]] += 1
      for i, ch in enumerate(characters):
        print(
          "{:>12s}: {} :: {}/{}/{}".format(
            ch,
            [int(x) for x in rgrouped[i]],
            bingrouped[i][-1],
            bingrouped[i][0],
            bingrouped[i][1],
          )
        )
    #"""
    α = kr_alpha(
      reliability_data = ratings,
      value_domain = list(range(7)),
      level_of_measurement = "ordinal"
    )
    α_binary = kr_alpha(
      reliability_data = bin_ratings,
      value_domain = [-1, 0, 1],
      level_of_measurement = "ordinal"
    )
    print(
      "  {:>22s}:  {:<8s} /   {:<8s}".format(
        t.split('.')[-1],
        "{:.3g}".format(α),
        "{:.3g}".format(α_binary)
      )
    )

if __name__ == "__main__":
  main(sys.stdin)
