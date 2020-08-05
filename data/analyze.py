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
  except ValueError:
    raise ValueError("Invalid index part: '{}'".format(index))

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
  #print("ZZZ", row)
  #print("QQQ", get(row, ".character.gendergroup"))
  #print("RRR", get(row, ".character.gendergroup") == "women")
  # TODO: DEBUG THIS?
  return get(row, ".character.gendergroup") == "women"

def character_male(row):
  return get(row, ".character.gendergroup") == "men"

def participant_female(row):
  return get(row, ".participant.gender_description") == "Female"

def infrequent_player(row):
  return get(row, ".participant.play_frequency") in ("never", "infrequent")

def is_lighter_skinned(row):
  return get(row, ".character.skin_tone") == "lighter"

def is_darker_skinned(row):
  return get(row, ".character.skin_tone") == "darker"

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

  ("Women:less-admirable", ".constructs.admirability", character_female, None, "-", {"controls": [".participant.id"]}),
  ("Japanese:more-admirable", ".constructs.admirability", is_japanese, None, "+", {"controls": [".participant.id"]}),

  ("Women:less-positive-gender", ".constructs.positive_gender_rep", character_female, None, "-", {"controls": [".participant.id"]}),

  ("Japanese:more-positive-ethnicity", ".constructs.positive_ethnic_rep", is_japanese, None, "+", {"controls": [".participant.id"]}),
  ("Majority:more-positive-ethnicity", ".constructs.positive_ethnic_rep", is_majority, None, "+", {"controls": [".participant.id"]}),
  ("Token:less-positive-ethnicity", ".constructs.positive_ethnic_rep", is_token, None, "-", {"controls": [".participant.id"]}),
]

#def primary_market_country(row):
#  return get(row, ".character.market") == "primary"

#def secondary_market_country(row):
#  return get(row, ".character.market") == "secondary"

def unknown_country(row):
  return get(row, ".character.country") == "Unknown"

def darker_skinned_women(row):
  return character_female(row) and get(row, ".character.skin_tone") == "darker"

def lighter_skinned_women(row):
  return character_female(row) and get(row, ".character.skin_tone") == "lighter"

def darker_skinned_men(row):
  return not character_female(row) and get(row, ".character.skin_tone") =="darker"

def lighter_skinned_men(row):
  return not character_female(row) and get(row, ".character.skin_tone") =="lighter"

#def secondary_market_women(row):
#  return character_female(row) and secondary_market_country(row)

#def primary_market_women(row):
#  return character_female(row) and primary_market_country(row)

#def secondary_market_men(row):
#  return not character_female(row) and secondary_market_country(row)

#def primary_market_men(row):
#  return not character_female(row) and primary_market_country(row)

def non_majority_women(row):
  return character_female(row) and not is_majority(row)

def majority_women(row):
  return character_female(row) and is_majority(row)

def non_majority_men(row):
  return character_male(row) and not is_majority(row)

def majority_men(row):
  return character_male(row) and is_majority(row)

def participant_nonwhite(row):
  return get(row, ".participant.normalized_ethnicity.White") == None

def ethnically_similar(row):
  return get(row, ".personal_ratings:1", 4) > 4

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
  ("Lighter:more-realistic", ".constructs.body_realism", is_lighter_skinned, is_darker_skinned, "+", {"controls": [".participant.id"]}),
  ("Lighter:more-attractive", ".constructs.attractiveness", is_lighter_skinned, is_darker_skinned, "+", {"controls": [".participant.id"]}),
  ("Lighter:less-muscular", ".constructs.muscles", is_lighter_skinned, is_darker_skinned, "-", {"controls": [".participant.id"]}),
  ("Lighter:thinner", ".constructs.thinness", is_lighter_skinned, is_darker_skinned, "+", {"controls": [".participant.id"]}),

  ("Majority-Nationality:more-realistic", ".constructs.body_realism", is_majority, None, "+", {"controls": [".participant.id"]}),
  ("Majority-Nationality:more-attractive", ".constructs.attractiveness", is_majority, None, "+", {"controls": [".participant.id"]}),
  ("Majority-Nationality:less-muscular", ".constructs.muscles", is_majority, None, "-", {"controls": [".participant.id"]}),
  ("Majority-Nationality:thinner", ".constructs.thinness", is_majority, None, "+", {"controls": [".participant.id"]}),

  # Ethnic sub-components (minus positive_ethnic_rep):
  ("Lighter:more-realistic-clothing", ".constructs.clothing_realism", is_lighter_skinned, is_darker_skinned, "+", {"controls": [".participant.id"]}),
  ("Lighter:less-obvious-ethnicity", ".constructs.combined_ethnic_signals", is_lighter_skinned, is_darker_skinned, "-", {"controls": [".participant.id"]}),

  ("Majority-Nationality:more-realistic-clothing", ".constructs.clothing_realism", is_majority, None, "+", {"controls": [".participant.id"]}),
  ("Majority-Nationality:less-obvious-ethnicity", ".constructs.combined_ethnic_signals", is_majority, None, "-", {"controls": [".participant.id"]}),

  # Villain sub-components
  ("Lighter:more-admirable", ".constructs.admirability", is_lighter_skinned, is_darker_skinned, "+", {"controls": [".participant.id"]}),
  ("Lighter:more-positive-ethnicity", ".constructs.positive_ethnic_rep", is_lighter_skinned, is_darker_skinned, "+", {"controls": [".participant.id"]}),
  ("Lighter:more-positive-gender", ".constructs.positive_gender_rep", is_lighter_skinned, is_darker_skinned, "+", {"controls": [".participant.id"]}),

  ("Majority-Nationality:more-admirable", ".constructs.admirability", is_majority, None, "+", {"controls": [".participant.id"]}),
  ("Majority-Nationality:more-positive-ethnicity", ".constructs.positive_ethnic_rep", is_majority, None, "+", {"controls": [".participant.id"]}),
  ("Majority-Nationality:more-positive-gender", ".constructs.positive_gender_rep", is_majority, None, "+", {"controls": [".participant.id"]}),

  # Intersections
  ("Lighter-Women:more-realistic", ".constructs.body_realism", lighter_skinned_women, darker_skinned_women, "+", {"controls": [".participant.id"]}),
  ("Lighter-Women:more-attractive", ".constructs.attractiveness", lighter_skinned_women, darker_skinned_women, "+", {"controls": [".participant.id"]}),
  ("Lighter-Women:less-sexualized", ".constructs.sexualization", lighter_skinned_women, darker_skinned_women, "-", {"controls": [".participant.id"]}),
  ("Lighter-Women:less-attire-sexualized", ".constructs.attire_sexualization", lighter_skinned_women, darker_skinned_women, "-", {"controls": [".participant.id"]}),
  ("Lighter-Women:less-muscular", ".constructs.muscles", lighter_skinned_women, darker_skinned_women, "-", {"controls": [".participant.id"]}),
  ("Lighter-Women:thinner", ".constructs.thinness", lighter_skinned_women, darker_skinned_women, "+", {"controls": [".participant.id"]}),
  ("Lighter-Women:older", ".constructs.youth", lighter_skinned_women, darker_skinned_women, "-", {"controls": [".participant.id"]}),
  ("Lighter-Women:more-admirable", ".constructs.admirability", lighter_skinned_women, darker_skinned_women, "+", {"controls": [".participant.id"]}),
  ("Lighter-Women:more-positive-gender", ".constructs.positive_gender_rep", lighter_skinned_women, darker_skinned_women, "+", {"controls": [".participant.id"]}),
  ("Lighter-Women:more-positive-ethnic", ".constructs.positive_ethnic_rep", lighter_skinned_women, darker_skinned_women, "+", {"controls": [".participant.id"]}),

  ("Majority-Nationality-Women:more-realistic", ".constructs.body_realism", majority_women, non_majority_women, "+", {"controls": [".participant.id"]}),
  ("Majority-Nationality-Women:more-attractive", ".constructs.attractiveness", majority_women, non_majority_women, "+", {"controls": [".participant.id"]}),
  ("Majority-Nationality-Women:less-sexualized", ".constructs.sexualization", majority_women, non_majority_women, "-", {"controls": [".participant.id"]}),
  ("Majority-Nationality-Women:less-attire-sexualized", ".constructs.attire_sexualization", majority_women, non_majority_women, "-", {"controls": [".participant.id"]}),
  ("Majority-Nationality-Women:less-muscular", ".constructs.muscles", majority_women, non_majority_women, "-", {"controls": [".participant.id"]}),
  ("Majority-Nationality-Women:thinner", ".constructs.thinness", majority_women, non_majority_women, "+", {"controls": [".participant.id"]}),
  ("Majority-Nationality-Women:older", ".constructs.youth", majority_women, non_majority_women, "-", {"controls": [".participant.id"]}),
  ("Majority-Nationality-Women:more-admirable", ".constructs.admirability", majority_women, non_majority_women, "+", {"controls": [".participant.id"]}),
  ("Majority-Nationality-Women:more-positive-gender", ".constructs.positive_gender_rep", majority_women, non_majority_women, "+", {"controls": [".participant.id"]}),
  ("Majority-Nationality-Women:more-positive-ethnic", ".constructs.positive_ethnic_rep", majority_women, non_majority_women, "+", {"controls": [".participant.id"]}),

  ("Lighter-Men:more-realistic", ".constructs.body_realism", lighter_skinned_men, darker_skinned_men, "+", {"controls": [".participant.id"]}),
  ("Lighter-Men:more-attractive", ".constructs.attractiveness", lighter_skinned_men, darker_skinned_men, "+", {"controls": [".participant.id"]}),
  ("Lighter-Men:less-muscular", ".constructs.muscles", lighter_skinned_men, darker_skinned_men, "-", {"controls": [".participant.id"]}),
  ("Lighter-Men:thinner", ".constructs.thinness", lighter_skinned_men, darker_skinned_men, "+", {"controls": [".participant.id"]}),
  ("Lighter-Men:older", ".constructs.youth", lighter_skinned_men, darker_skinned_men, "-", {"controls": [".participant.id"]}),
  ("Lighter-Men:more-admirable", ".constructs.admirability", lighter_skinned_men, darker_skinned_men, "+", {"controls": [".participant.id"]}),
  ("Lighter-Men:more-positive-gender", ".constructs.positive_gender_rep", lighter_skinned_men, darker_skinned_men, "+", {"controls": [".participant.id"]}),
  ("Lighter-Men:more-positive-ethnic", ".constructs.positive_ethnic_rep", lighter_skinned_men, darker_skinned_men, "+", {"controls": [".participant.id"]}),

  ("Majority-Nationality-Men:more-realistic", ".constructs.body_realism", majority_men, non_majority_men, "+", {"controls": [".participant.id"]}),
  ("Majority-Nationality-Men:more-attractive", ".constructs.attractiveness", majority_men, non_majority_men, "+", {"controls": [".participant.id"]}),
  ("Majority-Nationality-Men:less-muscular", ".constructs.muscles", majority_men, non_majority_men, "-", {"controls": [".participant.id"]}),
  ("Majority-Nationality-Men:thinner", ".constructs.thinness", majority_men, non_majority_men, "+", {"controls": [".participant.id"]}),
  ("Majority-Nationality-Men:older", ".constructs.youth", majority_men, non_majority_men, "-", {"controls": [".participant.id"]}),
  ("Majority-Nationality-Men:more-admirable", ".constructs.admirability", majority_men, non_majority_men, "+", {"controls": [".participant.id"]}),
  ("Majority-Nationality-Men:more-positive-gender", ".constructs.positive_gender_rep", majority_men, non_majority_men, "+", {"controls": [".participant.id"]}),
  ("Majority-Nationality-Men:more-positive-ethnic", ".constructs.positive_ethnic_rep", majority_men, non_majority_men, "+", {"controls": [".participant.id"]}),

  # Unknown dumping?
  ("Unknown:more-ethnic-cues", ".constructs.combined_ethnic_signals", unknown_country, None, "+", {"controls": [".participant.id"]}),
  ("Unknown:less-realistic", ".constructs.body_realism", unknown_country, None, "-", {"controls": [".participant.id"]}),
  ("Unknown:more-muscular", ".constructs.muscles", unknown_country, None, "+", {"controls": [".participant.id"]}),
  ("Unknown:less-attractive", ".constructs.attractiveness", unknown_country, None, "-", {"controls": [".participant.id"]}),
  ("Unknown:fatter", ".constructs.thinness", unknown_country, None, "-", {"controls": [".participant.id"]}),
  ("Unknown:older", ".constructs.youth", unknown_country, None, "-", {"controls": [".participant.id"]}),
  ("Unknown:less-admirable", ".constructs.admirability", unknown_country, None, "-", {"controls": [".participant.id"]}),
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

  ("Majority-Nationality:less-antisocial", ".character.motive.Antisocial", is_majority, None, '-', {"missing": 0}),
  ("Majority-Nationality:more-dominant", ".character.motive.Dominance", is_majority, None, '-', {"missing": 0}),
  ("Majority-Nationality:more-dutiful", ".character.motive.For Duty", is_majority, None, '+', {"missing": 0}),
  ("Majority-Nationality:less-woman-motivated", ".character.motive.For a Female", is_majority, None, '-', {"missing": 0}),
  ("Majority-Nationality:less-man-motivated", ".character.motive.For a Male", is_majority, None, '-', {"missing": 0}),
  ("Majority-Nationality:more-heroic", ".character.motive.Save the World", is_majority, None, '+', {"missing": 0}),

  ("Lighter-skinned:less-antisocial", ".character.motive.Antisocial", is_lighter_skinned, is_darker_skinned, '-', {"missing": 0}),
  ("Lighter-skinned:more-dominant", ".character.motive.Dominance", is_lighter_skinned, is_darker_skinned, '-', {"missing": 0}),
  ("Lighter-skinned:more-dutiful", ".character.motive.For Duty", is_lighter_skinned, is_darker_skinned, '+', {"missing": 0}),
  ("Lighter-skinned:less-woman-motivated", ".character.motive.For a Female", is_lighter_skinned, is_darker_skinned, '-', {"missing": 0}),
  ("Lighter-skinned:less-man-motivated", ".character.motive.For a Male", is_lighter_skinned, is_darker_skinned, '-', {"missing": 0}),
  ("Lighter-skinned:more-heroic", ".character.motive.Save the World", is_lighter_skinned, is_darker_skinned, '+', {"missing": 0}),
]

framedata_hypotheses = [
  # Men are bulkier
  ("Health:men-healthier", ".character.stats.health", character_male, character_female, '+'),
  ("Health:men-higher-dizzy", ".character.stats.dizzy", character_male, character_female, '+'),
  ("Size:men-grab-farther", ".character.stats.throw_range", character_male, character_female, '+'),
  # Women are more agile
  ("Agility:women-jump-higher", ".character.stats.jump_height", character_female, character_male, '+'),
  ("Agility:women-jump-farther", ".character.stats.jump_distance", character_female, character_male, '+'),
  ("Agility:women-dash-farther", ".character.stats.dash_distance", character_female, character_male, '+'),
  ("Agility:women-faster", ".character.stats.speed", character_female, character_male, '+'),
  # Men hit harder & slower
  ("Normals:men-more-damage", ".character.stats.normals.avg_hit_damage", character_male, character_female, '+'),
  ("Attacks:men-more-damage", ".character.stats.all_moves.avg_hit_damage", character_male, character_female, '+'),
  ("Normals:men-more-dizzy", ".character.stats.normals.avg_hit_dizzy", character_male, character_female, '+'),
  ("Attacks:men-more-dizzy", ".character.stats.all_moves.avg_hit_dizzy", character_male, character_female, '+'),
  ("Normals:men-active-longer", ".character.stats.normals.avg_active_frames", character_male, character_female, '+'),
  ("Attacks:men-active-longer", ".character.stats.all_moves.avg_active_frames", character_male, character_female, '+'),
  ("Normals:women-hit-more", ".character.stats.normals.avg_hit_count", character_female, character_male, '+'),
  ("Attacks:women-hit-more", ".character.stats.all_moves.avg_hit_count", character_female, character_male, '+'),
  ("Normals:men-slower", ".character.stats.normals.avg_frames_per_hit", character_male, character_female, '+'),
  ("Attacks:men-slower", ".character.stats.all_moves.avg_frames_per_hit", character_male, character_female, '+'),
  ("Normals:men-more-delayed", ".character.stats.normals.avg_dead_frames", character_male, character_female, '+'),
  ("Attacks:men-more-delayed", ".character.stats.all_moves.avg_dead_frames", character_male, character_female, '+'),
  ("Normals:men-more-hitstun", ".character.stats.normals.avg_hit_stun", character_male, character_female, '+'),
  ("Attacks:men-more-hitstun", ".character.stats.all_moves.avg_hit_stun", character_male, character_female, '+'),
  ("Normals:men-more-blockstun", ".character.stats.normals.avg_block_stun", character_male, character_female, '+'),
  ("Attacks:men-more-blockstun", ".character.stats.all_moves.avg_block_stun", character_male, character_female, '+'),
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
  # Darker-skinned characters are bulkier
  ("Health:darker-men-healthier", ".character.stats.health", darker_skinned_men, lighter_skinned_men, '+'),
  ("Health:darker-men-higher-dizzy", ".character.stats.dizzy", darker_skinned_men, lighter_skinned_men, '+'),
  ("Size:darker-men-grab-farther", ".character.stats.throw_range", darker_skinned_men, lighter_skinned_men, '+'),
  # Lighter-skinned characters are faster
  ("Agility:lighter-men-faster", ".character.stats.speed", lighter_skinned_men, darker_skinned_men, '+'),
  # Darker-skinned characters hit harder/slower
  ("Normals:darker-men-more-damage", ".character.stats.normals.avg_hit_damage", darker_skinned_men, lighter_skinned_men, '+'),
  ("Attacks:darker-men-more-damage", ".character.stats.all_moves.avg_hit_damage", darker_skinned_men, lighter_skinned_men, '+'),
  ("Normals:darker-men-more-dizzy", ".character.stats.normals.avg_hit_dizzy", darker_skinned_men, lighter_skinned_men, '+'),
  ("Attacks:darker-men-more-dizzy", ".character.stats.all_moves.avg_hit_dizzy", darker_skinned_men, lighter_skinned_men, '+'),
  ("Normals:darker-men-active-longer", ".character.stats.normals.avg_active_frames", darker_skinned_men, lighter_skinned_men, '+'),
  ("Attacks:darker-men-active-longer", ".character.stats.all_moves.avg_active_frames", darker_skinned_men, lighter_skinned_men, '+'),
  ("Normals:lighter-men-hit-more", ".character.stats.normals.avg_hit_count", lighter_skinned_men, darker_skinned_men, '+'),
  ("Attacks:lighter-men-hit-more", ".character.stats.all_moves.avg_hit_count", lighter_skinned_men, darker_skinned_men, '+'),
  ("Normals:darker-men-slower", ".character.stats.normals.avg_frames_per_hit", darker_skinned_men, lighter_skinned_men, '+'),
  ("Attacks:darker-men-slower", ".character.stats.all_moves.avg_frames_per_hit", darker_skinned_men, lighter_skinned_men, '+'),
  ("Normals:darker-men-more-delayed", ".character.stats.normals.avg_dead_frames", darker_skinned_men, lighter_skinned_men, '+'),
  ("Attacks:darker-men-more-delayed", ".character.stats.all_moves.avg_dead_frames", darker_skinned_men, lighter_skinned_men, '+'),
  ("Normals:darker-men-more-hitstun", ".character.stats.normals.avg_hit_stun", darker_skinned_men, lighter_skinned_men, '+'),
  ("Attacks:darker-men-more-hitstun", ".character.stats.all_moves.avg_hit_stun", darker_skinned_men, lighter_skinned_men, '+'),
  ("Normals:darker-men-more-blockstun", ".character.stats.normals.avg_block_stun", darker_skinned_men, lighter_skinned_men, '+'),
  ("Attacks:darker-men-more-blockstun", ".character.stats.all_moves.avg_block_stun", darker_skinned_men, lighter_skinned_men, '+'),
  ("Normals:lighter-men-plus-on-hit", ".character.stats.normals.avg_hit_advantage", lighter_skinned_men, darker_skinned_men, '+'),
  ("Attacks:lighter-men-plus-on-hit", ".character.stats.all_moves.avg_hit_advantage", lighter_skinned_men, darker_skinned_men, '+'),
  ("Normals:lighter-men-plus-on-block", ".character.stats.normals.avg_block_advantage", lighter_skinned_men, darker_skinned_men, '+'),
  ("Attacks:lighter-men-plus-on-block", ".character.stats.all_moves.avg_block_advantage", lighter_skinned_men, darker_skinned_men, '+'),
  ("Normals:lighter-men-more-multihit", ".character.stats.normals.multihit_proportion", lighter_skinned_men, darker_skinned_men, '+'),
  ("Attacks:lighter-men-more-multihit", ".character.stats.all_moves.multihit_proportion", lighter_skinned_men, darker_skinned_men, '+'),
  ("Normals:lighter-men-more-combos", ".character.stats.normals.combo_proportion", lighter_skinned_men, darker_skinned_men, '+'),
  ("Attacks:lighter-men-more-combos", ".character.stats.all_moves.combo_proportion", lighter_skinned_men, darker_skinned_men, '+'),
  ("Normals:darker-men-more-knockdowns", ".character.stats.normals.knockdown_proportion", darker_skinned_men, lighter_skinned_men, '+'),
  ("Attacks:darker-men-more-knockdowns", ".character.stats.all_moves.knockdown_proportion", darker_skinned_men, lighter_skinned_men, '+'),
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

#character_hypotheses = framedata_hypotheses

#all_hypotheses = full_hypotheses + character_hypotheses
# Looking at frame data statistically doesn't really make sense.
all_hypotheses = full_hypotheses

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
  "Majority-Nationality less exaggerated": [
    "Majority-Nationality:more-realistic",
    "Majority-Nationality:more-realistic-clothing",
    "Majority-Nationality:less-obvious-ethnicity",
  ],
  "Majority-Nationality less brutish": [
    "Majority-Nationality:less-muscular",
    "Majority-Nationality:thinner",
    "Majority-Nationality:more-attractive",
  ],
  "Majority-Nationality less villainous": [
    "Majority-Nationality:more-admirable",
    "Majority-Nationality:more-positive-ethnicity",
    "Majority-Nationality:more-positive-gender",
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
  "Lighter-skinned less exaggerated": [
    "Lighter:more-realistic",
    "Lighter:more-realistic-clothing",
    "Lighter:less-obvious-ethnicity",
  ],
  "Lighter-skinned less brutish": [
    "Lighter:less-muscular",
    "Lighter:thinner",
    "Lighter:more-attractive",
  ],
  "Lighter-skinned less villainous": [
    "Lighter:more-admirable",
    "Lighter:more-positive-ethnicity",
    "Lighter:more-positive-gender",
  ],
  "Lighter-skinned women more attractive/less sexualized then darker-skinned women":[
    "Lighter-Women:more-realistic",
    "Lighter-Women:less-muscular",
    "Lighter-Women:thinner",
    "Lighter-Women:older",
    "Lighter-Women:more-attractive",
    "Lighter-Women:less-sexualized",
    "Lighter-Women:less-attire-sexualized",
    "Lighter-Women:more-admirable",
    "Lighter-Women:more-positive-gender",
    "Lighter-Women:more-positive-ethnic",
  ],
  "Majority-Nationality women more attractive/less sexualized than Minority+Token-Nationality women": [
    "Majority-Nationality-Women:more-realistic",
    "Majority-Nationality-Women:less-muscular",
    "Majority-Nationality-Women:thinner",
    "Majority-Nationality-Women:older",
    "Majority-Nationality-Women:more-attractive",
    "Majority-Nationality-Women:less-sexualized",
    "Majority-Nationality-Women:less-attire-sexualized",
    "Majority-Nationality-Women:more-admirable",
    "Majority-Nationality-Women:more-positive-gender",
    "Majority-Nationality-Women:more-positive-ethnic",
  ],
  "Lighter-skinned men less brutish than darker-skinned men": [
    "Lighter-Men:more-realistic",
    "Lighter-Men:less-muscular",
    "Lighter-Men:thinner",
    "Lighter-Men:older",
    "Lighter-Men:more-attractive",
    "Lighter-Men:more-admirable",
    "Lighter-Men:more-positive-gender",
    "Lighter-Men:more-positive-ethnic",
  ],
  "Majority-Nationality men less brutish than Minority+Token-Nationality men": [
    "Majority-Nationality-Men:more-realistic",
    "Majority-Nationality-Men:less-muscular",
    "Majority-Nationality-Men:thinner",
    "Majority-Nationality-Men:older",
    "Majority-Nationality-Men:more-attractive",
    "Majority-Nationality-Men:more-admirable",
    "Majority-Nationality-Men:more-positive-gender",
    "Majority-Nationality-Men:more-positive-ethnic",
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
#  "Majority-Nationality 'better' motives":  [
#    "Majority-Nationality:less-antisocial",
#    "Majority-Nationality:more-dominant",
#    "Majority-Nationality:more-dutiful",
#    "Majority-Nationality:less-woman-motivated",
#    "Majority-Nationality:less-man-motivated",
#    "Majority-Nationality:more-heroic",
#  ],
#  "Lighter-skinned 'worse' motives":  [
#    "Lighter-skinned:less-antisocial",
#    "Lighter-skinned:more-dominant",
#    "Lighter-skinned:more-dutiful",
#    "Lighter-skinned:less-woman-motivated",
#    "Lighter-skinned:less-man-motivated",
#    "Lighter-skinned:more-heroic",
#  ],
  "Men are bulkier": [
    "Health:men-healthier",
    "Health:men-higher-dizzy",
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
    "Normals:men-more-dizzy",
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
    "Attacks:men-more-dizzy",
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
    "Health:darker-men-healthier",
    "Health:darker-men-higher-dizzy",
    "Size:darker-men-grab-farther",
  ],
  "Darker-skinned men are less agile": [
    "Agility:lighter-men-faster",
  ],
  "Darker-skinned men have slower/stronger normals": [
    "Normals:darker-men-more-damage",
    "Normals:darker-men-more-dizzy",
    "Normals:darker-men-active-longer",
    "Normals:lighter-men-hit-more",
    "Normals:darker-men-slower",
    "Normals:darker-men-more-delayed",
    "Normals:darker-men-more-hitstun",
    "Normals:darker-men-more-blockstun",
    "Normals:lighter-men-plus-on-hit",
    "Normals:lighter-men-plus-on-block",
    "Normals:lighter-men-more-multihit",
    "Normals:lighter-men-more-combos",
    "Normals:darker-men-more-knockdowns",
  ],
  "Darker-skinned men have slower/stronger attacks": [
    "Attacks:darker-men-more-damage",
    "Attacks:darker-men-more-dizzy",
    "Attacks:darker-men-active-longer",
    "Attacks:lighter-men-hit-more",
    "Attacks:darker-men-slower",
    "Attacks:darker-men-more-delayed",
    "Attacks:darker-men-more-hitstun",
    "Attacks:darker-men-more-blockstun",
    "Attacks:lighter-men-plus-on-hit",
    "Attacks:lighter-men-plus-on-block",
    "Attacks:lighter-men-more-multihit",
    "Attacks:lighter-men-more-combos",
    "Attacks:darker-men-more-knockdowns",
  ],
}

def main(fin):
  """
  Analyze the data from stdin.
  """
  print('='*80)
  print("Loading data...")
  data = json.loads(fin.read())
  print("Transforming data...")
  records = data["records"]
  fields = data["fields"]
  rows = []
  for r in records:
    row = { fields[i]: r[i] for i in range(len(fields)) }
    rows.append(row)
  print("Done setting up data.")

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
  # Dump into a file
  with open("analysis_results.json", 'w') as fout:
    json.dump([effects, expected], fout)
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
  trials=15000, # TODO: DEBUG
  #trials=15,
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
    # TODO: DEBUG
    print(
      pos_filter.__name__,
      [pos_filter(x) for x in rows[:5]],
      index,
      [get(x, index) for x in rows[:5]],
      ALIASES
    )
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
