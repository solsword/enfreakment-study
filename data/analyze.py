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

def get(row, index, default=None):
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
        return get(sub, rest, default)
      else:
        return default
    else:
      if isinstance(row, dict):
        return row.get(first, default)
      else:
        val = row[first]
        return val if val != None else default
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
  ("Japanese:more-realistic", ".constructs.body_realism", is_japanese, None, "+", {"controls": [".participant.id"]}),
  ("Women:less-muscular", ".constructs.muscles", character_female, None, "-", {"controls": [".participant.id"]}),
  ("Japanese:thinner", ".constructs.thinness", is_japanese, None, "+", {"controls": [".participant.id"]}),
  ("Women:thinner", ".constructs.thinness", character_female, None, "+", {"controls": [".participant.id"]}),

  ("Women:younger", ".constructs.youth", character_female, None, "+", {"controls": [".participant.id"]}),

  ("Women:more-attractive", ".constructs.attractiveness", character_female, None, "+", {"controls": [".participant.id"]}),
  ("Japanese:more-attractive", ".constructs.attractiveness", is_japanese, None, "+", {"controls": [".participant.id"]}),
  ("Majority:more-attractive", ".constructs.attractiveness", is_majority, None, "+", {"controls": [".participant.id"]}),
  ("Token:less-attractive", ".constructs.attractiveness", is_token, None, "-", {"controls": [".participant.id"]}),

  ("Women:more-sexualized", ".constructs.sexualization", character_female, None,"+", {"controls": [".participant.id"]}),
  ("Women:more-attire-sexualized", ".constructs.attire_sexualization", character_female, None,"+", {"controls": [".participant.id"]}),

  ("Women:less-realistic-clothes", ".constructs.clothing_realism", character_female, None, "-", {"controls": [".participant.id"]}),
  ("Japanese:more-realistic-clothes", ".constructs.clothing_realism", is_japanese, None, "+", {"controls": [".participant.id"]}),
  ("Majority:more-realistic-clothes", ".constructs.clothing_realism", is_majority, None, "+", {"controls": [".participant.id"]}),
  ("Token:less-realistic-clothes", ".constructs.clothing_realism", is_token, None, "-", {"controls": [".participant.id"]}),

  ("Women:more-obvious-ethnicity", ".constructs.combined_ethnic_signals", character_female, None,"+", {"controls": [".participant.id"]}),
  ("Japanese:less-obvious-ethnicity", ".constructs.combined_ethnic_signals", is_japanese, None, "-", {"controls": [".participant.id"]}),
  ("Majority:less-obvious-ethnicity", ".constructs.combined_ethnic_signals", is_majority, None,"-", {"controls": [".participant.id"]}),
  ("Token:more-obvious-ethnicity", ".constructs.combined_ethnic_signals", is_token, None, "+", {"controls": [".participant.id"]}),

  ("Women:less-admirable", ".constructs.admirableness", character_female, None, "-", {"controls": [".participant.id"]}),
  ("Japanese:more-admirable", ".constructs.admirableness", is_japanese, None, "+", {"controls": [".participant.id"]}),

  ("Women:less-positive-gender", ".constructs.positive_gender_rep", character_female, None, "-", {"controls": [".participant.id"]}),

  ("Japanese:more-positive-ethnicity", ".constructs.positive_ethnic_rep", is_japanese, None, "+", {"controls": [".participant.id"]}),
  ("Majority:more-positive-ethnicity", ".constructs.positive_ethnic_rep", is_majority, None, "+", {"controls": [".participant.id"]}),
  ("Token:less-positive-ethnicity", ".constructs.positive_ethnic_rep", is_token, None, "-", {"controls": [".participant.id"]}),
]

def primary_market_country(row):
  return get(row, ".character.market") == "primary"

def secondary_market_country(row):
  return get(row, ".character.market") == "secondary"

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

def secondary_market_women(row):
  return character_female(row) and secondary_market_country(row)

def primary_market_women(row):
  return character_female(row) and primary_market_country(row)

def secondary_market_men(row):
  return not character_female(row) and secondary_market_country(row)

def primary_market_men(row):
  return not character_female(row) and primary_market_country(row)

def participant_nonwhite(row):
  return get(row, ".participant.normalized_ethnicity.White") == None

def ethnically_similar(row):
  return get(row, ".personal_ratings:1", 4) > 4

def participant_minority(row):
  return (get(row, ".participant.normalized_ethnicity.White") == None) and any(
    [
      get(row, ".participant.normalized_ethnicity.Black"),
      get(row, ".participant.normalized_ethnicity.Native American"),
      get(row, ".participant.normalized_ethnicity.Hawaiian"),
      get(row, ".participant.normalized_ethnicity.Latinx"),
      get(row, ".participant.normalized_ethnicity.Hispanic"),
      get(row, ".participant.normalized_ethnicity.African"),
      get(row, ".participant.normalized_ethnicity.Puerto Rican"),
      get(row, ".participant.normalized_ethnicity.Hindu"),
      get(row, ".participant.normalized_ethnicity.Indian"),
      get(row, ".participant.normalized_ethnicity.Chinese"),
      get(row, ".participant.normalized_ethnicity.Korean"),
      get(row, ".participant.normalized_ethnicity.Persian"),
      get(row, ".participant.normalized_ethnicity.West Indian"),
      get(row, ".participant.normalized_ethnicity.Vietnamese"),
      get(row, ".participant.normalized_ethnicity.Filipino"),
      get(row, ".participant.normalized_ethnicity.Jewish"),
      get(row, ".participant.normalized_ethnicity.Polish"),
      get(row, ".participant.normalized_ethnicity.Finnish"),
      get(row, ".participant.normalized_ethnicity.Irish"),
    ]
  )

novel_hypotheses = [
  # Participant gender/frequency vs. gender perceptions:
  ("Female-Raters:recognize-bad-gender-rep", ".constructs.positive_gender_rep", participant_female, None, "-", {"controls": [".character.id"]}),
  ("Infrequent-Players:recognize-bad-gender-rep", ".constructs.positive_gender_rep", infrequent_player, None, "-", {"controls": [".character.id"]}),
  ("Frequent-Players:ignore-bad-gender-rep", ".constructs.positive_gender_rep", frequent_player, None, "+", {"controls": [".character.id"]}),

  # Participant ethnicity/frequency vs. ethnicity perceptions:
  ("Similar-Ethnicity:recognize-bad-ethnic-rep", ".constructs.positive_ethnic_rep", ethnically_similar, None, "-", {"controls": [".character.id"]}),
  ("Nonwhite-Raters:recognize-bad-ethnic-rep", ".constructs.positive_ethnic_rep", participant_nonwhite, None, "-", {"controls": [".character.id"]}),
  ("Infrequent-Players:recognize-bad-ethnic-rep", ".constructs.positive_ethnic_rep", infrequent_player, None, "-", {"controls": [".character.id"]}),
  ("Frequent-Players:ignore-bad-ethnic-rep", ".constructs.positive_ethnic_rep", frequent_player, None, "+", {"controls": [".character.id"]}),

  # Brute sub-components:
  ("Fair:more-realistic", ".constructs.body_realism", is_fair_skinned, is_dark_skinned, "+", {"controls": [".participant.id"]}),
  ("Fair:more-attractive", ".constructs.attractiveness", is_fair_skinned, is_dark_skinned, "+", {"controls": [".participant.id"]}),
  ("Fair:less-muscular", ".constructs.muscles", is_fair_skinned, is_dark_skinned, "-", {"controls": [".participant.id"]}),
  ("Fair:thinner", ".constructs.thinness", is_fair_skinned, is_dark_skinned, "+", {"controls": [".participant.id"]}),

  ("Primary-Market:more-realistic", ".constructs.body_realism", primary_market_country, secondary_market_country, "+", {"controls": [".participant.id"]}),
  ("Primary-Market:more-attractive", ".constructs.attractiveness", primary_market_country, secondary_market_country, "+", {"controls": [".participant.id"]}),
  ("Primary-Market:less-muscular", ".constructs.muscles", primary_market_country, secondary_market_country, "-", {"controls": [".participant.id"]}),
  ("Primary-Market:thinner", ".constructs.thinness", primary_market_country, secondary_market_country, "+", {"controls": [".participant.id"]}),

  # Ethnic sub-components (minus positive_ethnic_rep):
  ("Fair:more-realistic-clothing", ".constructs.clothing_realism", is_fair_skinned, is_dark_skinned, "+", {"controls": [".participant.id"]}),
  ("Fair:less-obvious-ethnicity", ".constructs.combined_ethnic_signals", is_fair_skinned, is_dark_skinned, "-", {"controls": [".participant.id"]}),

  ("Primary-Market:more-realistic-clothing", ".constructs.clothing_realism", primary_market_country, secondary_market_country, "+", {"controls": [".participant.id"]}),
  ("Primary-Market:less-obvious-ethnicity", ".constructs.combined_ethnic_signals", primary_market_country, secondary_market_country, "-", {"controls": [".participant.id"]}),

  # Villain sub-components
  ("Fair:more-admirable", ".constructs.admirableness", is_fair_skinned, is_dark_skinned, "+", {"controls": [".participant.id"]}),
  ("Fair:more-positive-ethnicity", ".constructs.positive_ethnic_rep", is_fair_skinned, is_dark_skinned, "+", {"controls": [".participant.id"]}),
  ("Fair:more-positive-gender", ".constructs.positive_gender_rep", is_fair_skinned, is_dark_skinned, "+", {"controls": [".participant.id"]}),

  ("Primary-Market:more-admirable", ".constructs.admirableness", primary_market_country, secondary_market_country, "+", {"controls": [".participant.id"]}),
  ("Primary-Market:more-positive-ethnicity", ".constructs.positive_ethnic_rep", primary_market_country, secondary_market_country, "+", {"controls": [".participant.id"]}),
  ("Primary-Market:more-positive-gender", ".constructs.positive_gender_rep", primary_market_country, secondary_market_country, "+", {"controls": [".participant.id"]}),

  # Intersections
  ("Fair-Women:more-realistic", ".constructs.body_realism", fair_skinned_women, dark_skinned_women, "+", {"controls": [".participant.id"]}),
  ("Fair-Women:more-attractive", ".constructs.attractiveness", fair_skinned_women, dark_skinned_women, "+", {"controls": [".participant.id"]}),
  ("Fair-Women:less-sexualized", ".constructs.sexualization", fair_skinned_women, dark_skinned_women, "-", {"controls": [".participant.id"]}),
  ("Fair-Women:less-attire-sexualized", ".constructs.attire_sexualization", fair_skinned_women, dark_skinned_women, "-", {"controls": [".participant.id"]}),
  ("Fair-Women:less-muscular", ".constructs.muscles", fair_skinned_women, dark_skinned_women, "-", {"controls": [".participant.id"]}),
  ("Fair-Women:thinner", ".constructs.thinness", fair_skinned_women, dark_skinned_women, "+", {"controls": [".participant.id"]}),
  ("Fair-Women:older", ".constructs.youth", fair_skinned_women, dark_skinned_women, "-", {"controls": [".participant.id"]}),
  ("Fair-Women:more-admirable", ".constructs.admirableness", fair_skinned_women, dark_skinned_women, "+", {"controls": [".participant.id"]}),
  ("Fair-Women:more-positive-gender", ".constructs.positive_gender_rep", fair_skinned_women, dark_skinned_women, "+", {"controls": [".participant.id"]}),
  ("Fair-Women:more-positive-ethnic", ".constructs.positive_ethnic_rep", fair_skinned_women, dark_skinned_women, "+", {"controls": [".participant.id"]}),

  ("Primary-Market-Women:more-realistic", ".constructs.body_realism", primary_market_women, secondary_market_women, "+", {"controls": [".participant.id"]}),
  ("Primary-Market-Women:more-attractive", ".constructs.attractiveness", primary_market_women, secondary_market_women, "+", {"controls": [".participant.id"]}),
  ("Primary-Market-Women:less-sexualized", ".constructs.sexualization", primary_market_women, secondary_market_women, "-", {"controls": [".participant.id"]}),
  ("Primary-Market-Women:less-attire-sexualized", ".constructs.attire_sexualization", primary_market_women, secondary_market_women, "-", {"controls": [".participant.id"]}),
  ("Primary-Market-Women:less-muscular", ".constructs.muscles", primary_market_women, secondary_market_women, "-", {"controls": [".participant.id"]}),
  ("Primary-Market-Women:thinner", ".constructs.thinness", primary_market_women, secondary_market_women, "+", {"controls": [".participant.id"]}),
  ("Primary-Market-Women:older", ".constructs.youth", primary_market_women, secondary_market_women, "-", {"controls": [".participant.id"]}),
  ("Primary-Market-Women:more-admirable", ".constructs.admirableness", primary_market_women, secondary_market_women, "+", {"controls": [".participant.id"]}),
  ("Primary-Market-Women:more-positive-gender", ".constructs.positive_gender_rep", primary_market_women, secondary_market_women, "+", {"controls": [".participant.id"]}),
  ("Primary-Market-Women:more-positive-ethnic", ".constructs.positive_ethnic_rep", primary_market_women, secondary_market_women, "+", {"controls": [".participant.id"]}),

  ("Fair-Men:more-realistic", ".constructs.body_realism", fair_skinned_men, dark_skinned_men, "+", {"controls": [".participant.id"]}),
  ("Fair-Men:more-attractive", ".constructs.attractiveness", fair_skinned_men, dark_skinned_men, "+", {"controls": [".participant.id"]}),
  ("Fair-Men:less-muscular", ".constructs.muscles", fair_skinned_men, dark_skinned_men, "-", {"controls": [".participant.id"]}),
  ("Fair-Men:thinner", ".constructs.thinness", fair_skinned_men, dark_skinned_men, "+", {"controls": [".participant.id"]}),
  ("Fair-Men:older", ".constructs.youth", fair_skinned_men, dark_skinned_men, "-", {"controls": [".participant.id"]}),
  ("Fair-Men:more-admirable", ".constructs.admirableness", fair_skinned_men, dark_skinned_men, "+", {"controls": [".participant.id"]}),
  ("Fair-Men:more-positive-gender", ".constructs.positive_gender_rep", fair_skinned_men, dark_skinned_men, "+", {"controls": [".participant.id"]}),
  ("Fair-Men:more-positive-ethnic", ".constructs.positive_ethnic_rep", fair_skinned_men, dark_skinned_men, "+", {"controls": [".participant.id"]}),

  ("Primary-Market-Men:more-realistic", ".constructs.body_realism", primary_market_men, secondary_market_men, "+", {"controls": [".participant.id"]}),
  ("Primary-Market-Men:more-attractive", ".constructs.attractiveness", primary_market_men, secondary_market_men, "+", {"controls": [".participant.id"]}),
  ("Primary-Market-Men:less-muscular", ".constructs.muscles", primary_market_men, secondary_market_men, "-", {"controls": [".participant.id"]}),
  ("Primary-Market-Men:thinner", ".constructs.thinness", primary_market_men, secondary_market_men, "+", {"controls": [".participant.id"]}),
  ("Primary-Market-Men:older", ".constructs.youth", primary_market_men, secondary_market_men, "-", {"controls": [".participant.id"]}),
  ("Primary-Market-Men:more-admirable", ".constructs.admirableness", primary_market_men, secondary_market_men, "+", {"controls": [".participant.id"]}),
  ("Primary-Market-Men:more-positive-gender", ".constructs.positive_gender_rep", primary_market_men, secondary_market_men, "+", {"controls": [".participant.id"]}),
  ("Primary-Market-Men:more-positive-ethnic", ".constructs.positive_ethnic_rep", primary_market_men, secondary_market_men, "+", {"controls": [".participant.id"]}),

  # Unknown dumping?
  ("Unknown:more-ethnic-cues", ".constructs.combined_ethnic_signals", unknown_country, None, "+", {"controls": [".participant.id"]}),
  ("Unknown:less-realistic", ".constructs.body_realism", unknown_country, None, "-", {"controls": [".participant.id"]}),
  ("Unknown:more-muscular", ".constructs.muscles", unknown_country, None, "+", {"controls": [".participant.id"]}),
  ("Unknown:less-attractive", ".constructs.attractiveness", unknown_country, None, "-", {"controls": [".participant.id"]}),
  ("Unknown:fatter", ".constructs.thinness", unknown_country, None, "-", {"controls": [".participant.id"]}),
  ("Unknown:older", ".constructs.youth", unknown_country, None, "-", {"controls": [".participant.id"]}),
  ("Unknown:less-admirable", ".constructs.admirableness", unknown_country, None, "-", {"controls": [".participant.id"]}),
  ("Unknown:worse-gender-rep", ".constructs.positive_gender_rep", unknown_country, None, "-", {"controls": [".participant.id"]}),
  ("Unknown:worse-ethnic-rep", ".constructs.positive_ethnic_rep", unknown_country, None, "-", {"controls": [".participant.id"]}),
]

motive_hypotheses = [
  # Motive hypotheses
  ("Women:less-antisocial", ".character.motive.Antisocial", character_female, None, '-', {"missing": 0}),
  ("Women:less-dominant", ".character.motive.Dominance", character_female, None, '-', {"missing": 0}),
  ("Women:less-dutiful", ".character.motive.For Duty", character_female, None, '-', {"missing": 0}),
  ("Women:less-woman-motivated", ".character.motive.For a Female", character_female, None, '-', {"missing": 0}),
  ("Women:more-man-motivated", ".character.motive.For a Male", character_female, None, '+', {"missing": 0}),
  ("Women:less-heroic", ".character.motive.Save the World", character_female, None, '-', {"missing": 0}),

  ("Primary-Market:less-antisocial", ".character.motive.Antisocial", primary_market_country, secondary_market_country, '-', {"missing": 0}),
  ("Primary-Market:more-dominant", ".character.motive.Dominance", primary_market_country, secondary_market_country, '-', {"missing": 0}),
  ("Primary-Market:more-dutiful", ".character.motive.For Duty", primary_market_country, secondary_market_country, '+', {"missing": 0}),
  ("Primary-Market:less-woman-motivated", ".character.motive.For a Female", primary_market_country, secondary_market_country, '-', {"missing": 0}),
  ("Primary-Market:less-man-motivated", ".character.motive.For a Male", primary_market_country, secondary_market_country, '-', {"missing": 0}),
  ("Primary-Market:more-heroic", ".character.motive.Save the World", primary_market_country, secondary_market_country, '+', {"missing": 0}),

  ("Fair-skinned:less-antisocial", ".character.motive.Antisocial", is_fair_skinned, is_dark_skinned, '-', {"missing": 0}),
  ("Fair-skinned:more-dominant", ".character.motive.Dominance", is_fair_skinned, is_dark_skinned, '-', {"missing": 0}),
  ("Fair-skinned:more-dutiful", ".character.motive.For Duty", is_fair_skinned, is_dark_skinned, '+', {"missing": 0}),
  ("Fair-skinned:less-woman-motivated", ".character.motive.For a Female", is_fair_skinned, is_dark_skinned, '-', {"missing": 0}),
  ("Fair-skinned:less-man-motivated", ".character.motive.For a Male", is_fair_skinned, is_dark_skinned, '-', {"missing": 0}),
  ("Fair-skinned:more-heroic", ".character.motive.Save the World", is_fair_skinned, is_dark_skinned, '+', {"missing": 0}),
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
  ("Normals:men-more-damage", ".character.stats.normals.avg_damage_per_hit", character_male, character_female, '+'),
  ("Attacks:men-more-damage", ".character.stats.all_moves.avg_damage_per_hit", character_male, character_female, '+'),
  ("Normals:men-more-stun", ".character.stats.normals.avg_stun_per_hit", character_male, character_female, '+'),
  ("Attacks:men-more-stun", ".character.stats.all_moves.avg_stun_per_hit", character_male, character_female, '+'),
  ("Normals:men-active-longer", ".character.stats.normals.avg_active_frames", character_male, character_female, '+'),
  ("Attacks:men-active-longer", ".character.stats.all_moves.avg_active_frames", character_male, character_female, '+'),
  ("Normals:women-hit-more", ".character.stats.normals.avg_hit_count", character_female, character_male, '+'),
  ("Attacks:women-hit-more", ".character.stats.all_moves.avg_hit_count", character_female, character_male, '+'),
  ("Normals:men-slower", ".character.stats.normals.avg_frames_per_hit", character_male, character_female, '+'),
  ("Attacks:men-slower", ".character.stats.all_moves.avg_frames_per_hit", character_male, character_female, '+'),
  ("Normals:men-more-delayed", ".character.stats.normals.avg_dead_frames", character_male, character_female, '+'),
  ("Attacks:men-more-delayed", ".character.stats.all_moves.avg_dead_frames", character_male, character_female, '+'),
  ("Normals:men-more-hitstun", ".character.stats.normals.avg_hitstun", character_male, character_female, '+'),
  ("Attacks:men-more-hitstun", ".character.stats.all_moves.avg_hitstun", character_male, character_female, '+'),
  ("Normals:men-more-blockstun", ".character.stats.normals.avg_blockstun", character_male, character_female, '+'),
  ("Attacks:men-more-blockstun", ".character.stats.all_moves.avg_blockstun", character_male, character_female, '+'),
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
  ("Normals:dark-men-more-damage", ".character.stats.normals.avg_damage_per_hit", dark_skinned_men, fair_skinned_men, '+'),
  ("Attacks:dark-men-more-damage", ".character.stats.all_moves.avg_damage_per_hit", dark_skinned_men, fair_skinned_men, '+'),
  ("Normals:dark-men-more-stun", ".character.stats.normals.avg_stun_per_hit", dark_skinned_men, fair_skinned_men, '+'),
  ("Attacks:dark-men-more-stun", ".character.stats.all_moves.avg_stun_per_hit", dark_skinned_men, fair_skinned_men, '+'),
  ("Normals:dark-men-active-longer", ".character.stats.normals.avg_active_frames", dark_skinned_men, fair_skinned_men, '+'),
  ("Attacks:dark-men-active-longer", ".character.stats.all_moves.avg_active_frames", dark_skinned_men, fair_skinned_men, '+'),
  ("Normals:fair-men-hit-more", ".character.stats.normals.avg_hit_count", fair_skinned_men, dark_skinned_men, '+'),
  ("Attacks:fair-men-hit-more", ".character.stats.all_moves.avg_hit_count", fair_skinned_men, dark_skinned_men, '+'),
  ("Normals:dark-men-slower", ".character.stats.normals.avg_frames_per_hit", dark_skinned_men, fair_skinned_men, '+'),
  ("Attacks:dark-men-slower", ".character.stats.all_moves.avg_frames_per_hit", dark_skinned_men, fair_skinned_men, '+'),
  ("Normals:dark-men-more-delayed", ".character.stats.normals.avg_dead_frames", dark_skinned_men, fair_skinned_men, '+'),
  ("Attacks:dark-men-more-delayed", ".character.stats.all_moves.avg_dead_frames", dark_skinned_men, fair_skinned_men, '+'),
  ("Normals:dark-men-more-hitstun", ".character.stats.normals.avg_hitstun", dark_skinned_men, fair_skinned_men, '+'),
  ("Attacks:dark-men-more-hitstun", ".character.stats.all_moves.avg_hitstun", dark_skinned_men, fair_skinned_men, '+'),
  ("Normals:dark-men-more-blockstun", ".character.stats.normals.avg_blockstun", dark_skinned_men, fair_skinned_men, '+'),
  ("Attacks:dark-men-more-blockstun", ".character.stats.all_moves.avg_blockstun", dark_skinned_men, fair_skinned_men, '+'),
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

full_hypotheses = (
  original_hypotheses
+ novel_hypotheses
)

# TODO: HERE?
#character_hypotheses = (
#  motive_hypotheses
#+ framedata_hypotheses
#)

character_hypotheses = framedata_hypotheses

hgroups = {
  "Women's ethnicity exaggerated": [
    "Women:less-realistic-clothes",
    "Women:more-obvious-ethnicity",
  ],
  "Women sexualized": [
    "Women:less-muscular",
    "Women:thinner",
    "Women:younger",
    "Women:more-attractive",
    "Women:more-sexualized",
    "Women:more-attire-sexualized",
  ],
  "Women disliked": [
    "Women:less-admirable",
    "Women:less-positive-gender",
  ],
  "Japanese more realistic": [
    "Japanese:more-realistic",
    "Japanese:more-realistic-clothes",
    "Japanese:less-obvious-ethnicity",
  ],
  "Japanese preferred": [
    "Japanese:thinner",
    "Japanese:more-attractive",
    "Japanese:more-admirable",
    "Japanese:more-positive-ethnicity",
  ],
  "Primary-Market less exaggerated": [
    "Primary-Market:more-realistic",
    "Primary-Market:more-realistic-clothing",
    "Primary-Market:less-obvious-ethnicity",
  ],
  "Primary-Market less brutish": [
    "Primary-Market:less-muscular",
    "Primary-Market:thinner",
    "Primary-Market:more-attractive",
  ],
  "Primary-Market less villainous": [
    "Primary-Market:more-admirable",
    "Primary-Market:more-positive-ethnicity",
    "Primary-Market:more-positive-gender",
  ],
  "Majority preferred/realistic": [
    "Majority:more-realistic-clothes",
    "Majority:less-obvious-ethnicity",
    "Majority:more-attractive",
    "Majority:more-positive-ethnicity",
  ],
  "Token suppressed/unrealistic": [
    "Token:less-realistic-clothes",
    "Token:more-obvious-ethnicity",
    "Token:less-attractive",
    "Token:less-positive-ethnicity",
  ],
  "Unknown country used for villains/brutes": [
    "Unknown:more-ethnic-cues",
    "Unknown:less-realistic",
    "Unknown:more-muscular",
    "Unknown:fatter",
    "Unknown:older",
    "Unknown:less-attractive",
    "Unknown:less-admirable",
    "Unknown:worse-gender-rep",
    "Unknown:worse-ethnic-rep",
  ],
  "Fair-skinned less exaggerated": [
    "Fair:more-realistic",
    "Fair:more-realistic-clothing",
    "Fair:less-obvious-ethnicity",
  ],
  "Fair-skinned less brutish": [
    "Fair:less-muscular",
    "Fair:thinner",
    "Fair:more-attractive",
  ],
  "Fair-skinned less villainous": [
    "Fair:more-admirable",
    "Fair:more-positive-ethnicity",
    "Fair:more-positive-gender",
  ],
  "Fair-skinned women more attractive/less sexualized then dark-skinned women":[
    "Fair-Women:more-realistic",
    "Fair-Women:less-muscular",
    "Fair-Women:thinner",
    "Fair-Women:older",
    "Fair-Women:more-attractive",
    "Fair-Women:less-sexualized",
    "Fair-Women:less-attire-sexualized",
    "Fair-Women:more-admirable",
    "Fair-Women:more-positive-gender",
    "Fair-Women:more-positive-ethnic",
  ],
  "Primary-Market women more attractive/less sexualized than Secondary-Market women": [
    "Primary-Market-Women:more-realistic",
    "Primary-Market-Women:less-muscular",
    "Primary-Market-Women:thinner",
    "Primary-Market-Women:older",
    "Primary-Market-Women:more-attractive",
    "Primary-Market-Women:less-sexualized",
    "Primary-Market-Women:less-attire-sexualized",
    "Primary-Market-Women:more-admirable",
    "Primary-Market-Women:more-positive-gender",
    "Primary-Market-Women:more-positive-ethnic",
  ],
  "Fair-skinned men less brutish than dark-skinned men": [
    "Fair-Men:more-realistic",
    "Fair-Men:less-muscular",
    "Fair-Men:thinner",
    "Fair-Men:older",
    "Fair-Men:more-attractive",
    "Fair-Men:more-admirable",
    "Fair-Men:more-positive-gender",
    "Fair-Men:more-positive-ethnic",
  ],
  "Primary-Market men less brutish than Secondary-Market men": [
    "Primary-Market-Men:more-realistic",
    "Primary-Market-Men:less-muscular",
    "Primary-Market-Men:thinner",
    "Primary-Market-Men:older",
    "Primary-Market-Men:more-attractive",
    "Primary-Market-Men:more-admirable",
    "Primary-Market-Men:more-positive-gender",
    "Primary-Market-Men:more-positive-ethnic",
  ],
  "Women and non-gamers more aware of gender stereotypes": [
    "Female-Raters:recognize-bad-gender-rep",
    "Infrequent-Players:recognize-bad-gender-rep",
    "Frequent-Players:ignore-bad-gender-rep",
  ],
  "Nonwhite and non-gamers more aware of racial stereotypes": [
    "Similar-Ethnicity:recognize-bad-ethnic-rep",
    "Nonwhite-Raters:recognize-bad-ethnic-rep",
    "Infrequent-Players:recognize-bad-ethnic-rep",
    "Frequent-Players:ignore-bad-ethnic-rep",
  ],
#  "Women 'worse' motives":  [
#    "Women:less-antisocial",
#    "Women:less-dominant",
#    "Women:less-dutiful",
#    "Women:less-woman-motivated",
#    "Women:more-man-motivated",
#    "Women:less-heroic",
#  ],
#  "Primary-market 'better' motives":  [
#    "Primary-Market:less-antisocial",
#    "Primary-Market:more-dominant",
#    "Primary-Market:more-dutiful",
#    "Primary-Market:less-woman-motivated",
#    "Primary-Market:less-man-motivated",
#    "Primary-Market:more-heroic",
#  ],
#  "Fair-skinned 'worse' motives":  [
#    "Fair-skinned:less-antisocial",
#    "Fair-skinned:more-dominant",
#    "Fair-skinned:more-dutiful",
#    "Fair-skinned:less-woman-motivated",
#    "Fair-skinned:less-man-motivated",
#    "Fair-skinned:more-heroic",
#  ],
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
    "Normals:men-more-hitstun",
    "Normals:men-more-blockstun",
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
    "Attacks:men-more-hitstun",
    "Attacks:men-more-blockstun",
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
    "Normals:dark-men-more-hitstun",
    "Normals:dark-men-more-blockstun",
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
    "Attacks:dark-men-more-hitstun",
    "Attacks:dark-men-more-blockstun",
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
    "Testing {} full hypotheses using {}...".format(
      len(full_hypotheses),
      use.__name__
    )
  )
  tests = init_tests(rows, full_hypotheses, use)
  print('-'*80)
  print(
    "Testing {} character hypotheses using {}...".format(
      len(character_hypotheses),
      use.__name__
    )
  )
  char_tests = init_tests(rows, character_hypotheses, use, char=True)
  print('-'*80)
  effects, expected = analyze_tests(rows, tests + char_tests)
  print('-'*80)
  summarize_tests(effects, expected, hgroups)
  print('-'*80)
  analyze_agreement(rows)
  print('-'*80)
  print("...analysis complete.")
  print('='*80)

class Undefined:
  pass

def bootstrap_test(
  rows,
  index,
  pos_filter,
  alt_filter=None,
  extras=None,
  trials=15000,
  seed=1081230891
):
  if not extras:
    extras = {}
  controls = extras.get("controls", [])
  missing = extras.get("missing", Undefined)
  pos_mean = 0
  pos_count = 0
  alt_mean = 0
  alt_count = 0
  nones = 0
  groups = {}
  for i, row in enumerate(rows):
    val = get(row, index)
    ident = '=' + "::".join(str(get(row, ctrl)) for ctrl in controls)
    if val == None and missing != Undefined:
      val = missing
    elif val == None:
      nones += 1
      continue
    if ident not in groups:
      groups[ident] = [[], [], []]
    vals, hits, alts = groups[ident]
    vals.append(val)
    if pos_filter(row):
      hits.append(len(vals) - 1)
      pos_mean += val
      pos_count += 1
    elif alt_filter == None:
      alts.append(len(vals) - 1)
      alt_mean += val
      alt_count += 1

    if alt_filter != None and alt_filter(row):
      alts.append(len(vals) - 1)
      alt_mean += val
      alt_count += 1

  if pos_count == 0:
    return None, "No positive examples found!"

  if alt_count == 0:
    return None, "No alternate examples found!"

  pos_mean /= pos_count
  alt_mean /= alt_count

  md = pos_mean - alt_mean

  if (md == 0):
    # no need to simulate anything; all trials would have
    # abs(mean difference) >= 0
    return 0, 1

  random.seed(seed)
  as_diff = 0
  for t in range(trials):
    pos_mean = 0
    alt_mean = 0
    for g in groups:
      vals, hits, alts = groups[g]
      random.shuffle(vals)
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
  alt_filter=None,
  extras=None,
):
  # TODO: Implement extras here!?!
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

def init_tests(rows, hypotheses, method=bootstrap_test, char=False):
  """
  Constructs a bunch of test objects and returns a list of them for
  analyze_tests to process.
  """
  tests = []
  if char: # simplify rows to one/character (just use first)
    seen = set()
    crows = []
    for row in rows:
      cid = get(row, ".character.id")
      if cid not in seen:
        seen.add(cid)
        crows.append(row)
      # else continue
    rows = crows

  for i, hyp in enumerate(hypotheses):
    if len(hyp) == 5: # no extras
      name, index, pos_filter, alt_filter, direction = hyp
      extras = {}
    else: # has extras
      name, index, pos_filter, alt_filter, direction, extras = hyp
    md, p = method(rows, index, pos_filter, alt_filter, extras)
    prg = "{}/{} done [{}]...".format(i, len(hypotheses), name)
    print(prg, " "*(78 - len(prg)), end="\r")
    sys.stdout.flush()

    dword = {
      "+": "greater",
      "-": "less"
    }[direction]

    cond_name = pos_filter.__name__

    iname = index.split('.')[-1]
    if md == None: # test error
      tests.append(
        [
          name,
          None,
          None,
          1,
          None,
          "{} {} for {}? {}".format(iname, dword, cond_name, p)
        ]
      )
    elif direction == "+":
      smsg = "== {} is greater for {}: {:+.3g}, p = {:.3g}".format(
        iname,
        cond_name,
        md,
        p
      )
      fmsg = "-- {} is indistinguishable for {}: p = {:.3g}".format(
        iname,
        cond_name,
        p
      )
      qmsg = "!! {} is unexpectedly smaller for {}: {:+.3g}, p = {:.3g}".format(
        iname,
        cond_name,
        md,
        p
      )
      qfmsg = "-- {} is indistinguishable (& unexpectedly smaller) for {}: p = {:.3g}".format(
        iname,
        cond_name,
        p
      )
      if md > 0:
        tests.append([name, True, md, p, smsg, fmsg])
      else:
        tests.append([name, False, md, p, qmsg, qfmsg])
    elif direction == "-":
      smsg = "== {} is smaller for {}: {:+.3g}, p = {:.3g}".format(
        iname,
        cond_name,
        md,
        p
      )
      fmsg = "-- {} is indistinguishable for {}: p = {:.3g}".format(
        iname,
        cond_name,
        p
      )
      qmsg = "!! {} is unexpectedly greater for {}: {:+.3g}, p = {:.3g}".format(
        iname,
        cond_name,
        md,
        p
      )
      qfmsg = "-- {} is indistinguishable (& unexpectedly greater) for {}: p = {:.3g}".format(
        iname,
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
    error = md == None
    close = p < threshold if not isinstance(p, str) else False
    expected[name] = expd
    if error:
      e = "ERR: {}".format(fmsg)
      effects[name] = e
      print(e)
    elif failed:
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
      if expected[hyp] == None:
        print("  {}: {}".format(hyp, effects[hyp]))
      else:
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
    pidmap = {}
    nextpid = 0
    for row in rows:
      pid = get(row, ".participant.id")
      if pid in pidmap:
        ipid = pidmap[pid]
      else:
        ipid = nextpid
        pidmap[pid] = ipid
        nextpid += 1
      ch = get(row, ".character.id")
      cid = charmap[ch]
      if not np.isnan(ratings[ipid, cid]):
        print(
          "Double-fill: [{}, {}] was {} ? {}!".format(
            ipid,
            ch,
            ratings[ipid, cid],
            np.isnan(ratings[ipid, cid])
          ),
          file=sys.stderr
        )
        print(row, file=sys.stderr)
      val = get(row, t)
      ratings[ipid,cid] = val
      bin_ratings[ipid,cid] = [-1,0,1][(val>3) + (val>4)] if val else None
    # DEBUG:
    """
    if "muscular" in t:
      rgrouped = {i: [] for i in range(len(characters))}
      bingrouped = {i: { -1: 0, 0: 0, 1: 0 } for i in range(len(characters))}
      for ipid in range(ratings.shape[0]):
        for cid in range(ratings.shape[1]):
          if not np.isnan(ratings[ipid,cid]):
            rgrouped[cid].append(ratings[ipid,cid])
          if not np.isnan(bin_ratings[ipid,cid]):
            bingrouped[cid][bin_ratings[ipid,cid]] += 1
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
