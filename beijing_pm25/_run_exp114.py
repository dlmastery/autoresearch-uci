"""Exp114 — CatBoost Plain add is_janfeb on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add is_janfeb on Exp97 (CatBoost cycle 40/50)",
    "--add-feature", "is_janfeb",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire compares 2013 val "
        "persist to 2014, not last fire's 10 bomb hours. New: 2013 val persist RMSE is "
        "24.50 versus 2014 test 22.32, so 2013 is the harder year. Exp97 skill is +9.5 "
        "percent on val versus +7.1 percent on test. 2013 January persist 37.47 mean "
        "166.8 with 138 hours persist>=300 versus 39 such hours in 2014. 2013 February "
        "persist 38.30 versus 2014 February 26.01. is_heating lumps Nov-Dec (2013 persist "
        "23-29) with Jan-Feb (37-38). roll3mean missed val. Bomb-chasing and weather "
        "increments stay closed."
    ),
    "--citations",
    (
        "Zhang, Qiang; He, Kebin and Huo, Hong 2012 Nature 'Cleaning China's air' — "
        "northern-China residential coal peaks in the coldest months, so January-February "
        "is a different emission regime than the November-December shoulder already "
        "covered by is_heating. Relevance: 2013 val persist is 24.50 versus 2014 test "
        "22.32 because January 2013 mean PM is 166.8 with 138 persist>=300 hours and "
        "February persist is 38.30, and is_janfeb is one change from Exp97, not another "
        "rolling persist mean after pm25_roll3mean missed 2013 val."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding is_janfeb, a binary equal to 1 in January and "
        "February, to the Exp97 CatBoost Plain recipe (depth 6, learning_rate 0.03, "
        "l2_leaf_reg 3, rh_magnus plus dewp_delta plus is_heating plus 24 lags) will "
        "cut 2013 val RMSE because the mechanism is isolating peak-heating mega-winter "
        "from the Nov-Dec shoulder so 2013 January-February is not mixed with milder "
        "heating months. Per Zhang et al. 2012 that is peak winter coal. Because "
        "roll3mean just failed, this is the unused peak-heating calendar flag not another "
        "persist smoother. KEEP if 1h composite beats -22.167. This single change starts "
        "from the current champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. 2013 val may move from 22.167 toward 21.90 to "
        "22.20 if Jan-Feb isolation helps. A val RMSE above 22.25 is a miss. Ranges are "
        "ug/m3 on the frozen 2014 timestamps."
    ),
])
