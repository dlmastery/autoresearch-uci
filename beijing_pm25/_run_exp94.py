"""Exp94 — CatBoost Plain add cbwd_prev_NW on Exp91 rh_magnus 1h recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add cbwd_prev_NW on Exp91 rh_magnus (CatBoost cycle 20/50)",
    "--backbone", "catboost",
    "--add-feature", "rh_magnus",
    "--add-feature", "cbwd_prev_NW",
    "--set", "iterations=2000",
    "--set", "depth=6",
    "--set", "learning_rate=0.03",
    "--set", "l2_leaf_reg=3",
    "--set", "early_stopping_rounds=100",
    "--set", "boosting_type=Plain",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp91 residuals on high-PRES dirty hours, "
        "not last fire's hour-10 blob. Exp91 val 22.449 is 0.052 from KEEP. New: "
        "PRES>=1025 persist>=150 n=413 RMSE 44.27 versus Exp30 41.59 and persist-1 40.56 "
        "skill -9.1 percent. Model over-cleans pred_d -12.2 versus need -3.2. On that slice "
        "with no previous-hour NW n=277 RMSE 43.72 versus persist 38.64 need +1.73 pred_d "
        "-7.07. cv persist>=150 n=505 RMSE 29.15 versus persist 27.68. Iws<2 persist>=150 "
        "n=739 RMSE 31.10 versus persist 29.83. rsm and l2 stay closed."
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
        "— stagnant synoptic weather plus regional transport, not a local emission spike, "
        "builds Beijing haze, so last-hour NW is the clean-fetch memory current cbwd_NW "
        "drops when the wind dies. Relevance: Exp91 still RMSE 43.72 versus persist-1 "
        "38.64 on PRES>=1025 persist>=150 hours with no previous-hour NW on the frozen "
        "2014 nowcast, and adding cbwd_prev_NW is one change from Exp91, not another rsm "
        "or l2."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding cbwd_prev_NW, the previous-hour NW dummy, to the Exp91 "
        "CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, rh_magnus plus "
        "inversion_spread plus pm25_delta1 plus 24 lags) will cut 2013 val RMSE because "
        "the mechanism is one oblivious split on last-hour NW so high-PRES dirty hours "
        "that are not a just-arrived clean surge are not treated as frontal cleanout. Per "
        "Huang et al. 2014 that synoptic type is the trap versus the fetch. Because rsm "
        "and l2 already failed val, this is previous-direction memory not another HP. "
        "KEEP if 1h composite beats -22.397. This single change starts from the current "
        "champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.6 to 21.8 versus Exp30 20.945, val 22.05 to 22.60, and "
        "composite -22.70 to -22.05. PRES>=1025 persist>=150 RMSE may move from 44.27 "
        "toward 40.0 to 43.0 versus persist-1 40.56. A val RMSE above 22.55 is a miss. "
        "Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
