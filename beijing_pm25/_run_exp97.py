"""Exp97 — CatBoost Plain add is_heating on Exp96 rh_magnus+dewp_delta 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add is_heating on Exp96 dewp_delta (CatBoost cycle 23/50)",
    "--add-feature", "is_heating",
    "--diagnosis",
    (
        "1h champion is now Exp96 CatBoost: test 20.881, val 22.357 so val is still the "
        "bottleneck, January 34.94 versus persist-1 33.58 and JJA 14.05, hour 20 32.51, "
        "onset n=83 RMSE 110.32 losing to persist-1 107.80. This fire recomputes Exp96 "
        "January and hour-1 cuts, not last fire's Friday dewpoint-rise blob. New: January "
        "RH>=70 n=84 RMSE 38.25 versus Exp30 29.59 and persist-1 23.94 (skill -59.8 "
        "percent), over-cleans pred_d -9.21 versus need -3.87. January Iws<2 n=227 RMSE "
        "34.91 versus persist 29.42. January hour-1 n=28 RMSE 76.95 versus persist 69.40, "
        "need +8.32 pred_d -5.35 wrong sign. Hour-1 outside January is 20.63 versus "
        "persist 20.60 so the hour-1 hole is January. month_sin already failed. rsm l2 "
        "and wind dummy stay closed."
    ),
    "--citations",
    (
        "Huang, Ru-Jin; Zhang, Yanlin; Bozzetti, Carlo; Ho, Kin-Fai; Cao, Jun-Ji; "
        "Han, Yongming; Daellenbach, Kaspar R.; Slowik, Jay G.; Platt, Stephen M.; "
        "Canonaco, Francesco; Zotter, Peter; Wolf, Robert; Pieber, Simone M.; Bruns, "
        "Emily A.; Crippa, Monica; Ciarelli, Giancarlo; Piazzalunga, Andrea; "
        "Schwikowski, Margit; Abbaszade, Gulcin; Schnelle-Kreis, Juergen; Zimmermann, "
        "Ralf; An, Zhisheng; Szidat, Soenke; Baltensperger, Urs; El Haddad, Imad and "
        "Prevot, Andre S. H. 2014 Nature 'High secondary aerosol contribution to "
        "particulate pollution during haze events in China' (doi:10.1038/nature13774) "
        "— winter haze under moist stagnation is secondary production, not the wet "
        "removal high RH marks in summer, so a heating-season flag keeps January RH "
        "from sharing the JJA scavenge cut. Relevance: Exp96 still RMSE 38.25 versus "
        "persist-1 23.94 on January RH>=70 hours on the frozen 2014 nowcast, and adding "
        "is_heating is one change from Exp96, not another moisture derivative."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding is_heating, the Nov-Feb binary, to the Exp96 CatBoost "
        "Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, rh_magnus plus "
        "dewp_delta plus inversion_spread plus 24 lags) will cut 2013 val RMSE because "
        "the mechanism is one oblivious split on heating season so January RH>=70 hours "
        "are not scored like JJA wet-scavenge. Per Huang et al. 2014 that winter moist "
        "state is secondary haze not washout. Because month_sin already failed and "
        "dewp_delta just KEEPed, this is the unused winter flag not another RH formula. "
        "KEEP if 1h composite beats -22.357. This single change starts from the current "
        "champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.5 to 21.6 versus Exp96 20.881, val 22.00 to 22.50, and "
        "composite -22.55 to -22.00. January RH>=70 RMSE may move from 38.25 toward 24.0 "
        "to 32.0 versus persist-1 23.94. A val RMSE above 22.45 is a miss. Ranges are "
        "ug/m3 on the frozen 2014 timestamps."
    ),
])
