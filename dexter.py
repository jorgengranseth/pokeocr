import json
import constraint

import numpy as np

dm = {
    200: np.array([1, 2]),
        400: np.array([3, 4]),
        600: np.array([5, 6]),
        800: np.array([7, 8]),
        1000: np.array([9, 10]),
        1300: np.array([11, 12]),
        1600: np.array([13, 14]),
        1900: np.array([15, 16]),
        2200: np.array([17, 18]),
        2500: np.array([19, 20]),
        3000: np.array([21, 22]),
        3500: np.array([23, 24]),
        4000: np.array([25, 26]),
        4500: np.array([27, 28]),
        5000: np.array([29, 30]),
        6000: np.array([31, 32]),
        7000: np.array([33, 34]),
        8000: np.array([35, 36]),
        9000: np.array([37, 38]),
        10000: np.array([39, 40])
}

lvl_mods = np.array([ 0.094     ,  0.16639787,  0.21573247,  0.25572005,  0.29024988,
        0.3210876 ,  0.34921268,  0.37523559,  0.39956728,  0.42250001,
        0.44310755,  0.46279839,  0.48168495,  0.49985844,  0.51739395,
        0.53435433,  0.55079269,  0.56675452,  0.58227891,  0.59740001,
        0.61215729,  0.62656713,  0.64065295,  0.65443563,  0.667934  ,
        0.68116492,  0.69414365,  0.70688421,  0.71939909,  0.7317    ,
        0.73776948,  0.74378943,  0.74976104,  0.75568551,  0.76156384,
        0.76739717,  0.7731865 ,  0.77893275,  0.78463697,  0.79030001],
        dtype=np.float32)

STAMINA = "Stamina"
ATTACK = "Attack"
DEFENCE = "Defence"

pokedex = json.load(open("dex3.json"))

def get_stats(pokename):
    stats = pokedex[pokename]

    attack = stats[ATTACK]
    defence = stats[DEFENCE]
    stamina = stats[STAMINA]

    return np.array([attack, defence, stamina], dtype=np.float32)



MAX_IV = 15

def cpc(vals, lm):
    a, d, s = vals
    return np.floor(a * np.sqrt(d) * np.sqrt(s) * lm**2 / 10.0)

def calculate_ivs(pokename, cp, hp, dust):
    base_vals = get_stats(pokename)

    possible_levels = dm[dust]
    possible_lvl_indices = possible_levels - 1
    lm = lvl_mods[possible_lvl_indices]

    problem = constraint.Problem()
    problem.addVariables(['att_iv', 'def_iv', 'sta_iv'], range(16))
    problem.addConstraint(lambda att_iv, def_iv, sta_iv:
            hp in np.floor((base_vals[-1] + sta_iv) * lm))
    problem.addConstraint(lambda att_iv, def_iv, sta_iv:
            cp in cpc(base_vals + np.array([att_iv, def_iv, sta_iv]), lm))

    return problem.getSolutions()


if __name__ == "__main__":
    pokename = "Charmander"
    cp = 151
    hp = 28
    dust = 600

    for solution in calculate_ivs(pokename, cp, hp, dust):
        a = solution['sta_iv']
        d = solution['def_iv']
        s = solution['att_iv']

        print "Attack: {:>2d} - Defence: {:>2d} - Stamina: {:>2d}".format(a, d, s)
