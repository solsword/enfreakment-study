#!/usr/bin/env python3

import json
import csv
import sys
import random

idmap = {
  "abigail": "Abigail",
  "akuma": "Akuma",
  "alex": "Alex",
  "balrog": "Balrog",
  "birdie": "Birdie",
  "cammy": "Cammy",
  "chun_li": "Chun-Li",
  "dhalsim": "Dhalsim",
  "ed": "Ed",
  "f_a_n_g": "F.A.N.G",
  "guile": "Guile",
  "ibuki": "Ibuki",
  "juri": "Juri",
  "karin": "Karin",
  "ken": "Ken",
  "kolin": "Kolin",
  "laura": "Laura",
  "m_bison": "M.Bison",
  "menat": "Menat",
  "nash": "Nash",
  "necalli": "Necalli",
  "rashid": "Rashid",
  "r_mika": "R.Mika",
  "ryu": "Ryu",
  "urien": "Urien",
  "vega": "Vega",
  "zangief": "Zangief",
  "zeku": ("Zeku (Old)", "Zeku (Young)"),
}

weights = "LMH"
buttons = "PK"
stances = ["stand", "crouch"]

normals = [
  "{} {}{}".format(stance, weight, button)
    for stance in stances
    for weight in weights
    for button in buttons
]

skin_tones = {
  "abigail": "fair",
  "akuma": "dark",
  "alex": "fair",
  "balrog": "dark",
  "birdie": "dark",
  "cammy": "fair",
  "chun_li": "fair",
  "dhalsim": "dark",
  "ed": "fair",
  "f_a_n_g": "fair",
  "guile": "fair",
  "ibuki": "fair",
  "juri": "fair",
  "karin": "fair",
  "ken": "fair",
  "kolin": "fair",
  "laura": "dark",
  "m_bison": "fair",
  "menat": "dark",
  "nash": "fair",
  "necalli": "dark",
  "rashid": "fair",
  "r_mika": "fair",
  "ryu": "fair",
  "urien": "dark",
  "vega": "fair",
  "zangief": "fair",
  "zeku": "fair",
}

alt_tones = {
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
}

def men(x):
  return x["gender"] == "male"
def women(x):
  return x["gender"] == "female"
def fair_skinned(x):
  return x["skin_tone"] == "fair"
def dark_skinned(x):
  return x["skin_tone"] == "dark"

hypotheses = [
  # Men are more healthy
  ["health", men, women],
  ["stun", men, women],
  # Women are more agile
  ["jump_height", women, men],
  ["jump_distance", women, men],
  ["dash_distance", women, men],
  ["speed", women, men],
  # Men are larger
  ["throw_range", men, women],
  # Men hit harder & slower
  ["avg_hit_damage", men, women],
  ["avg_hit_stun", men, women],
  ["avg_active_frames", men, women],
  ["avg_hit_count", women, men],
  ["avg_frames_per_hit", men, women],
  ["avg_dead_frames", men, women],
  ["avg_hit_advantage", women, men],
  ["avg_block_advantage", women, men],
  ["multihit_proportion", women, men],
  ["combo_proportion", women, men],
  ["knockdown_proportion", men, women],
  # Men have safer attacks
  ["unsafe_proportion", women, men],
  # Dark-skinned characters are beefier
  ["health", dark_skinned, fair_skinned],
  ["stun", dark_skinned, fair_skinned],
  # Dark-skinned characters hit harder/slower
  ["speed", fair_skinned, dark_skinned],
  ["avg_hit_damage", dark_skinned, fair_skinned],
  ["avg_hit_stun", dark_skinned, fair_skinned],
  ["avg_active_frames", dark_skinned, fair_skinned],
  ["avg_hit_count", fair_skinned, dark_skinned],
  ["avg_frames_per_hit", dark_skinned, fair_skinned],
  ["avg_dead_frames", dark_skinned, fair_skinned],
  ["avg_hit_advantage", fair_skinned, dark_skinned],
  ["avg_block_advantage", fair_skinned, dark_skinned],
  ["multihit_proportion", fair_skinned, dark_skinned],
  ["combo_proportion", fair_skinned, dark_skinned],
  ["knockdown_proportion", dark_skinned, fair_skinned],
]


combined_tones = {
  k: (
    ["dark", "indeterminate", "fair"][
      int(skin_tones[k] == "fair") + int(alt_tones[k] == "fair")
    ]
  )
    for k in skin_tones.keys()
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

def bootstrap_test(
  items,
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
  slippage = 0
  for i, item in enumerate(items):
    val = item.get(index)
    if val == None:
      slippage += 1
      continue
    vals.append(val)
    if pos_filter(item):
      hits.append(i - slippage)
      pos_mean += val
      pos_count += 1
    elif alt_filter == None:
      alts.append(i - slippage)
      alt_mean += val
      alt_count += 1

    if alt_filter != None and alt_filter(item):
      alts.append(i - slippage)
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

def average_missing(*vals):
  result = 0
  missing = False
  for v in vals:
    if v == None:
      missing = True
      break
    result += v
  if missing:
    return None
  else:
    return result / len(vals)

def sum_missing(*vals):
  result = 0
  missing = False
  for v in vals:
    if v == None:
      missing = True
      break
    result += v
  if missing:
    return None
  else:
    return result

def jump_height(x):
  if x == "?":
    return None
  hs = x[:x.index("(")].strip()
  if hs:
    return float(hs)
  else:
    return sum(float(b) for b in x[1:-1].split('+'))

def stat_value(x):
  if type(x) == str:
    if x in ['?', '~', '-']:
      return None
    elif '+' in x:
      return sum(float(b) for b in x.split('+'))
    elif '(' in x:
      return float(x[:x.index('(')])
    else:
      return float(x)
  elif x is None:
    return x
  else:
    return float(x)

def active_frames(x):
  if type(x) == str:
    if '*' in x:
      active = [float(b) for b in x.split('*')]
      gaps = [0]*(len(active)-1)
      return (active, gaps)
    else:
      try:
        active = []
        gaps = []
        norm = x.replace(")", "_").replace("(", "_")
        bits = norm.split("_")
        for i, b in enumerate(bits):
          if i % 2 == 0:
            active.append(float(b))
          else:
            gaps.append(float(b))
        return (active, gaps)
      except:
        raise ValueError("Bad active frames value: '{}'".format(x))
  return ([x], [])

def on_hit(x):
  if type(x) == str:
    if "KD" in x:
      return "knockdown"
    elif x in ["?", "~"]:
      return None
    elif '/' in x:
      return min(float(b) for b in x.split('/'))
  else:
    return x

def damage_values(x):
  if type(x) == str:
    if x in "?~":
      return None
    else:
      bits = x.split("*")
      result = []
      for b in bits:
        if "(" in b:
          b = b[:b.index("(")]
        result.append(float(b))
      return result
  else:
    return [x]

def move_info(data):
  st = stat_value(data.get("startup", None))
  act, gaps = active_frames(data.get("active", None))
  rec = stat_value(data.get("recovery", None))
  onhit = on_hit(data.get("onHit", None))
  onblock = on_hit(data.get("onBlock", None))
  knockdown = False
  if onhit == "knockdown":
    knockdown = True
    onhit = None
  dmg = damage_values(data["damage"])
  stn = damage_values(data["stun"])
  hits = len(dmg)
  return {
    "hits": hits,
    "multihit": hits > 1,
    "damage": dmg,
    "stun": stn,
    "frames_per_hit": sum_missing(*([st, rec] + act + gaps)) / hits,
    "dead_frames": sum_missing(st, rec),
    "active_frames": act,
    "advantage_on_hit": onhit,
    "advantage_on_block": onblock,
    "can_combo": None if onhit is None else onhit > 0,
    "unsafe": None if onblock is None else onblock < 0,
    "knockdown": knockdown,
  }

def div(x):
  return (x[0] / x[1]) if x[1] > 0 else None

def analyze(ch, cdata):
  """
  Analyze data for a single character to compute average startup frames, active
  frames, recovery frames, on hit/block frame advantage, and knockdown
  potential.
  """
  print("Analyzing {}...".format(ch))
  result = { "id": ch }
  # Base stats
  base_stats = cdata["stats"]
  result["health"] = stat_value(base_stats.get("health", None))
  result["stun"] = stat_value(base_stats.get("stun", None))
  result["jump_height"] = average_missing(
    jump_height(base_stats.get("nJump", None)),
    jump_height(base_stats.get("fJump", None)),
    jump_height(base_stats.get("bJump", None)),
  )
  result["jump_distance"] = average_missing(
    stat_value(base_stats.get("fJumpDist", None)),
    stat_value(base_stats.get("bJumpDist", None))
  )
  result["dash_distance"] = average_missing(
    stat_value(base_stats.get("fDashDist", None)),
    stat_value(base_stats.get("bDashDist", None))
  )
  result["speed"] = average_missing(
    stat_value(base_stats.get("fWalk", None)),
    stat_value(base_stats.get("bWalk", None))
  )
  result["throw_range"] = stat_value(base_stats["throwRange"])

  # Normal moves
  movedata = cdata["moves"]["normal"]
  move_avg = {
    "hits": [0, 0],
    "frames_per_hit": [0, 0],
    "dead_frames": [0, 0],
    "advantage_on_hit": [0, 0],
    "advantage_on_block": [0, 0],
  }
  move_cmb = {
    "damage": [0, 0],
    "stun": [0, 0],
    "active_frames": [0, 0],
  }
  move_prp = {
    "multihit": [0, 0],
    "can_combo": [0, 0],
    "unsafe": [0, 0],
    "knockdown": [0, 0],
  }
  for n in normals:
    cn = n[0].capitalize() + n[1:]
    if n in movedata:
      vals = [ move_info(movedata[n]) ]
    elif cn in movedata:
      vals = [ move_info(movedata[cn]) ]
    else:
      matches = [k for k in movedata if k.startswith(n) or k.startswith(cn)]
      if matches:
        vals = [move_info(movedata[m]) for m in matches]
      else:
        print(
          "Missing move data: {} → '{}' ('{}')".format(ch, n, cn),
          file=sys.stderr
        )
        continue

    for valset in vals:
      for k in move_avg:
        v = valset[k]
        if v != None:
          move_avg[k][0] += v
          move_avg[k][1] += 1

      for k in move_cmb:
        for v in valset[k]:
          if v != None:
            move_cmb[k][0] += v
            move_cmb[k][1] += 1

      for k in move_prp:
        v = valset[k]
        if v != None:
          move_prp[k][0] += 1 if v else 0
          move_prp[k][1] += 1

  result["avg_hit_damage"] = div(move_cmb["damage"])
  result["avg_hit_stun"] = div(move_cmb["stun"])
  result["avg_active_frames"] = div(move_cmb["active_frames"])

  result["avg_hit_count"] = div(move_avg["hits"])
  result["avg_frames_per_hit"] = div(move_avg["frames_per_hit"])
  result["avg_dead_frames"] = div(move_avg["dead_frames"])
  result["avg_hit_advantage"] = div(move_avg["advantage_on_hit"])
  result["avg_block_advantage"] = div(move_avg["advantage_on_block"])

  result["multihit_proportion"] = div(move_prp["multihit"])
  result["combo_proportion"] = div(move_prp["can_combo"])
  result["unsafe_proportion"] = div(move_prp["unsafe"])
  result["knockdown_proportion"] = div(move_prp["knockdown"])

  return result

def main():
  define_cprops()
  with open("characterData.json", 'r') as fin:
    data = json.load(fin)

  chstats = {}
  for ch in idmap:
    result = {}
    if isinstance(idmap[ch], (list, tuple)):
      for cid in idmap[ch]:
        stats = analyze(ch, data[cid])
        for key in stats:
          if key in result:
            if result[key] == None or stats[key] == None:
              result[key] = None
            elif isinstance(result[key], (int, float)):
              result[key] += stats[key]
            elif result[key] != stats[key]:
              raise ValueError(
                "Inconsistent within-character values for '{}': {} != {}"
                .format(
                  key,
                  result[key],
                  stats[key]
                )
              )
            # else keep original value (e.g. for 'id')
          else:
            result[key] = stats[key]
      for key in stats:
        if isinstance(result[key], (int, float)):
          result[key] /= len(idmap[ch])
    else:
      result = analyze(ch, data[idmap[ch]])

    for key in result:
      print("  {}: {}".format(key, result[key]))

    result["gender"] = CPROPS[ch]["gender"]
    result["skin_tone"] = combined_tones[ch]
    chstats[ch] = result

  print("Testing hypotheses...")
  for index, pos, alt in hypotheses:
    md, p = bootstrap_test([chstats[ch] for ch in chstats], index, pos, alt)
    expected = md > 0
    if p < 0.05:
      if md > 0:
        print(
          "  {}: {} > {} ({:.3g}; p={:.3g})".format( 
            index,
            pos.__name__,
            alt.__name__,
            md,
            p
          )
        )
      elif md == 0:
        print(
          "! {}: {} = {}".format( 
            index,
            pos.__name__,
            alt.__name__
          )
        )
      else:
        print(
          "! {}: {} < {} ({:.3g}; p={:.3g})".format( 
            index,
            pos.__name__,
            alt.__name__,
            md,
            p
          )
        )
    else:
      print(
        "  {}: no significant results for {} vs. {}".format(
          index, 
          pos.__name__,
          alt.__name__,
        )
      )

if __name__ == "__main__":
  main()
