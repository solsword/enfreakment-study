#!/usr/bin/env python3
"""
process.py

Processes data from all_chars.csv and characterData.json to test hypotheses
about character design bias in frame data.

Get characterData.json from:
  https://fullmeter.com/fatonline/lib/characterData.json

Full app that we're using data from:
  https://fullmeter.com/fatonline/#/framedata/
"""

import json
import csv
import sys
import random

#P_THRESHOLD = 0.2
P_THRESHOLD = 0.05

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

columns = [
  "id",
  "health",
  "dizzy",
  "jump_height",
  "jump_distance",
  "dash_distance",
  "speed",
  "throw_range",

  "normals.avg_hit_damage",
  "normals.avg_hit_dizzy",
  "normals.avg_active_frames",

  "normals.avg_hit_count",
  "normals.avg_frames_per_hit",
  "normals.avg_dead_frames",
  "normals.avg_hit_stun",
  "normals.avg_block_stun",
  "normals.avg_hit_advantage",
  "normals.avg_block_advantage",

  "normals.multihit_proportion",
  "normals.combo_proportion",
  "normals.unsafe_proportion",
  "normals.knockdown_proportion",
  "normals.knockdown_count",

  "all_moves.avg_hit_damage",
  "all_moves.avg_hit_dizzy",
  "all_moves.avg_active_frames",

  "all_moves.avg_hit_count",
  "all_moves.avg_frames_per_hit",
  "all_moves.avg_dead_frames",
  "all_moves.avg_hit_stun",
  "all_moves.avg_block_stun",
  "all_moves.avg_hit_advantage",
  "all_moves.avg_block_advantage",

  "all_moves.multihit_proportion",
  "all_moves.combo_proportion",
  "all_moves.unsafe_proportion",
  "all_moves.knockdown_proportion",
  "all_moves.knockdown_count",
]

skin_tones = {
  "abigail": "lighter",
  "akuma": "darker",
  "alex": "lighter",
  "balrog": "darker",
  "birdie": "darker",
  "cammy": "lighter",
  "chun_li": "lighter",
  "dhalsim": "darker",
  "ed": "lighter",
  "f_a_n_g": "lighter",
  "guile": "lighter",
  "ibuki": "lighter",
  "juri": "lighter",
  "karin": "lighter",
  "ken": "lighter",
  "kolin": "lighter",
  "laura": "darker",
  "m_bison": "lighter",
  "menat": "darker",
  "nash": "lighter",
  "necalli": "darker",
  "rashid": "lighter",
  "r_mika": "lighter",
  "ryu": "lighter",
  "urien": "darker",
  "vega": "lighter",
  "zangief": "lighter",
  "zeku": "lighter",
}

alt_tones = {
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
}

def men(x):
  return x["gender"] == "male"

def women(x):
  return x["gender"] == "female"

def lighter_skinned(x):
  return x["skin_tone"] == "lighter"

def darker_skinned(x):
  return x["skin_tone"] == "darker"

hypotheses = [
  # Men are more healthy
  ["health", men, women],
  ["dizzy", men, women],
  # Women are more agile
  ["jump_height", women, men],
  ["jump_distance", women, men],
  ["dash_distance", women, men],
  ["speed", women, men],
  # Men are larger
  ["throw_range", men, women],
  # Men hit harder & slower
  ["normals.avg_hit_damage", men, women],
  ["normals.avg_hit_dizzy", men, women],
  ["normals.avg_active_frames", men, women],
  ["normals.avg_hit_count", women, men],
  ["normals.avg_frames_per_hit", men, women],
  ["normals.avg_dead_frames", men, women],
  ["normals.avg_hit_advantage", women, men],
  ["normals.avg_block_advantage", women, men],
  ["normals.multihit_proportion", women, men],
  ["normals.combo_proportion", women, men],
  ["normals.knockdown_proportion", men, women],
  # Men have safer attacks
  ["normals.unsafe_proportion", women, men],
  # Dark-skinned characters are beefier
  ["health", darker_skinned, lighter_skinned],
  ["dizzy", darker_skinned, lighter_skinned],
  # Dark-skinned characters hit harder/slower
  ["speed", lighter_skinned, darker_skinned],
  ["normals.avg_hit_damage", darker_skinned, lighter_skinned],
  ["normals.avg_hit_dizzy", darker_skinned, lighter_skinned],
  ["normals.avg_active_frames", darker_skinned, lighter_skinned],
  ["normals.avg_hit_count", lighter_skinned, darker_skinned],
  ["normals.avg_frames_per_hit", darker_skinned, lighter_skinned],
  ["normals.avg_dead_frames", darker_skinned, lighter_skinned],
  ["normals.avg_hit_advantage", lighter_skinned, darker_skinned],
  ["normals.avg_block_advantage", lighter_skinned, darker_skinned],
  ["normals.multihit_proportion", lighter_skinned, darker_skinned],
  ["normals.combo_proportion", lighter_skinned, darker_skinned],
  ["normals.knockdown_proportion", darker_skinned, lighter_skinned],
]


combined_tones = {
  k: (
    ["darker", "indeterminate", "lighter"][
      int(skin_tones[k] == "lighter") + int(alt_tones[k] == "lighter")
    ]
  )
    for k in skin_tones.keys()
}

CPROPS = None
CPFILE = "all_chars.csv"

TSVFILE = "framedata.tsv"
JSONFILE = "framedata.json"

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
      if '.' in index:
        outer, inner = index.split('.')
        val = item[outer].get(inner)
        if val == None:
          slippage += 1
          continue
      else:
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

  if pos_count == 0:
    raise ValueError(
      "No positive examples for '{}' ('{}' vs. '{}')".format(
        index,
        pos_filter.__name__,
        '<rest>' if alt_filter == None else alt_filter.__name__
      )
    )
  if alt_count == 0:
    raise ValueError(
      "No alternate examples for '{}' ('{}' vs. '{}')".format(
        index,
        pos_filter.__name__,
        '<rest>' if alt_filter == None else alt_filter.__name__
      )
    )

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
      bits = x.split('+')
      vals = [float(b) for b in bits if b.strip().isdigit()]
      return sum(vals)
    elif '*' in x:
      bits = x.split('*')
      vals = [float(b) for b in bits if b.strip().isdigit()]
      return sum(vals)
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
      active = []
      gaps = []
      bits = x.split('*')
      for i, b in enumerate(bits):
        subact, subgaps = active_frames(b)
        active.extend(subact)
        gaps.extend(subgaps)
        if i < len(bits) - 1:
          gaps.append(0)
      return (active, gaps)
    elif x == '~':
      return ([0], [])
    else:
      try:
        active = []
        gaps = []
        norm = x.replace(")", "_").replace("(", "_")
        bits = norm.split("_")
        for i, b in enumerate(bits):
          if b in ('', '~') and i == len(bits) - 1:
            # ignore blank or ~ at end
            continue
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
    if " per dagger" in x:
      x = x[:x.index(" per dagger")]

    if "(" in x:
      x = x[:x.index("(")]

    if '/' in x:
      x = x[:x.index("/")]

    if x in "?~":
      return None
    elif '+' in x:
      bits = x.split('+')
      result = []
      for b in bits:
        result.extend(damage_values(b))
      return result
    else:
      bits = x.split("*")
      result = []
      for b in bits:
        if 'x' in b:
          first, second = b.split('x')
          b = float(first) * float(second)
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
  if onblock == "knockdown":
    knockdown = True
    onblock = None
  dmg = damage_values(data["damage"]) if "damage" in data else None
  dzy = damage_values(data["stun"]) if "stun" in data else None
  hits = len(dmg) if dmg else 0
  return {
    "hits": hits,
    "multihit": hits > 1,
    "damage": dmg,
    "dizzy": dzy,
    "frames_per_hit": div([sum_missing(*([st, rec or 0] + act + gaps)), hits]),
    "dead_frames": sum_missing(st, rec or 0),
    "active_frames": act,
    "block_stun": None if (onblock is None or rec is None) else rec + onblock,
    "hit_stun": None if (onhit is None or rec is None) else rec + onhit,
    "advantage_on_hit": onhit,
    "advantage_on_block": onblock,
    "can_combo": None if onhit is None else onhit > 0,
    "unsafe": None if onblock is None else onblock < 0,
    "knockdown": knockdown,
  }

def div(x):
  return (x[0] / x[1]) if (x[1] > 0 and x[0] != None) else None

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
  result["dizzy"] = stat_value(base_stats.get("stun", None))
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
  result["normals"] = collect_moves_stats(cdata["moves"]["normal"], normals)

  # All moves
  allmoves = {}
  for group in cdata["moves"]:
    for move in cdata["moves"][group]:
      allmoves[group + "|" + move] = cdata["moves"][group][move]

  result["all_moves"] = collect_moves_stats(allmoves)

  return result

def collect_moves_stats(movedata, move_keys=None):
  """
  Averages various values from moves in the given moves dictionary. If
  move_keys is given, it only uses moves that match those keys, with a bit of
  leeway for inexact matches.
  """

  result = {}

  move_avg = {
    "hits": [0, 0],
    "frames_per_hit": [0, 0],
    "dead_frames": [0, 0],
    "hit_stun": [0, 0],
    "block_stun": [0, 0],
    "advantage_on_hit": [0, 0],
    "advantage_on_block": [0, 0],
  }
  move_cmb = {
    "damage": [0, 0],
    "dizzy": [0, 0],
    "active_frames": [0, 0],
  }
  move_prp = {
    "multihit": [0, 0],
    "can_combo": [0, 0],
    "unsafe": [0, 0],
    "knockdown": [0, 0],
  }

  if move_keys != None:
    keys = move_keys
  else:
    keys = movedata.keys()

  for mk in keys:
    cmk = mk[0].capitalize() + mk[1:]
    if mk in movedata:
      vals = [ move_info(movedata[mk]) ]
    elif cmk in movedata:
      vals = [ move_info(movedata[cmk]) ]
    else:
      matches = [k for k in movedata if k.startswith(mk) or k.startswith(cmk)]
      if matches:
        vals = [move_info(movedata[m]) for m in matches]
      else:
        print(
          "Missing move data: {} -> '{}' ('{}')".format(ch, mk, cmk),
          #file=sys.stderr
        )
        continue

    for valset in vals:
      for k in move_avg:
        if valset[k] != None:
          v = valset[k]
          if v != None:
            move_avg[k][0] += v
            move_avg[k][1] += 1

      for k in move_cmb:
        if valset[k] != None:
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
  result["avg_hit_dizzy"] = div(move_cmb["dizzy"])
  result["avg_active_frames"] = div(move_cmb["active_frames"])

  result["avg_hit_count"] = div(move_avg["hits"])
  result["avg_frames_per_hit"] = div(move_avg["frames_per_hit"])
  result["avg_dead_frames"] = div(move_avg["dead_frames"])
  result["avg_hit_stun"] = div(move_avg["hit_stun"])
  result["avg_block_stun"] = div(move_avg["block_stun"])
  result["avg_hit_advantage"] = div(move_avg["advantage_on_hit"])
  result["avg_block_advantage"] = div(move_avg["advantage_on_block"])

  result["multihit_proportion"] = div(move_prp["multihit"])
  result["combo_proportion"] = div(move_prp["can_combo"])
  result["unsafe_proportion"] = div(move_prp["unsafe"])
  result["knockdown_proportion"] = div(move_prp["knockdown"])
  result["knockdown_count"] = move_prp["knockdown"][0]

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
              result[key] += stats[key] # will be divided later to get avg
            elif isinstance(result[key], dict):
              rsub = result[key]
              ssub = stats[key]
              for subkey in ssub:
                if subkey in rsub:
                  if rsub[subkey] == None or ssub[subkey] == None:
                    rsub[subkey] = None
                  elif isinstance(rsub[subkey], (int, float)):
                    rsub[subkey] += ssub[subkey] # divided later to get avg
                  elif rsub[subkey] != ssub[subkey]:
                    raise ValueError(
                      (
                        "Inconsistent within-character subvalues for '{}'->"
                      + "'{}': {} != {}"
                      ).format(
                        key,
                        subkey,
                        rsub[subkey],
                        ssub[subkey]
                      )
                    )
                  # else keep original sub-value as they're the same
                else:
                  rsub[subkey] = ssub[subkey]
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
        elif isinstance(result[key], dict):
          for subkey in result[key]:
            if isinstance(result[key][subkey], (int, float)):
              result[key][subkey] /= len(idmap[ch])
    else:
      result = analyze(ch, data[idmap[ch]])

    for key in result:
      print("  {}: {}".format(key, result[key]))

    result["gender"] = CPROPS[ch]["gender"]
    result["skin_tone"] = combined_tones[ch]
    chstats[ch] = result

  print("Writing TSV...")
  with open(TSVFILE, 'w') as fout:
    writer = csv.writer(fout, dialect="excel-tab")
    writer.writerow(columns)
    for ch in sorted(idmap):
      stats = chstats[ch]
      row = []
      for col in columns:
        if col in stats:
          row.append(stats[col])
        elif '.' in col:
          outer, inner = col.split('.')
          row.append(stats[outer][inner])
        else:
          raise ValueError("Invalid column: '{}'".format(col))
      writer.writerow(row)

  print("Writing JSON...")
  with open(JSONFILE, 'w') as fout:
    json.dump(chstats, fout)

  print("Pullout comparisons...")
  male_kdps = []
  female_kdps = []
  male_kdcs = []
  female_kdcs = []
  for ch in chstats:
    stats = chstats[ch]
    if stats["gender"] == "male":
      male_kdps.append(stats["normals"]["knockdown_proportion"])
      male_kdcs.append(stats["normals"]["knockdown_count"])
    elif stats["gender"] == "female":
      female_kdps.append(stats["normals"]["knockdown_proportion"])
      female_kdcs.append(stats["normals"]["knockdown_count"])

  nmkdp = min(male_kdps)
  xmkdp = max(male_kdps)
  amkdp = sum(male_kdps) / len(male_kdps)
  nfkdp = min(female_kdps)
  xfkdp = max(female_kdps)
  afkdp = sum(female_kdps) / len(female_kdps)
  print("  % of normals with knockdown:")
  print(
    "      men: {}% ({}%--{}%)".format(
      round(100*amkdp, 1),
      round(100*nmkdp, 1),
      round(100*xmkdp, 1)
    )
  )
  print(
    "    women: {}% ({}%--{}%)".format(
      round(100*afkdp, 1),
      round(100*nfkdp, 1),
      round(100*xfkdp, 1)
    )
  )

  nmkdc = min(male_kdcs)
  xmkdc = max(male_kdcs)
  amkdc = sum(male_kdcs) / len(male_kdcs)
  nfkdc = min(female_kdcs)
  xfkdc = max(female_kdcs)
  afkdc = sum(female_kdcs) / len(female_kdcs)
  print("  # of normals with knockdown:")
  print("      men: {} ({}--{})".format(round(amkdc, 3), nmkdc, xmkdc))
  print("    women: {} ({}--{})".format(round(afkdc, 3), nfkdc, xfkdc))

  print("Characters with != 1 knockdown normal:")
  for ch in chstats:
    stats = chstats[ch]
    kds = stats["normals"]["knockdown_count"]
    if kds != 1:
      print(
        "  {} ({}/{}): {}".format(
          stats["id"],
          stats["gender"],
          stats["skin_tone"],
          kds
        )
      )

  print("Testing hypotheses...")
  for index, pos, alt in hypotheses:
    md, p = bootstrap_test([chstats[ch] for ch in chstats], index, pos, alt)
    expected = md > 0
    if p < P_THRESHOLD:
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
