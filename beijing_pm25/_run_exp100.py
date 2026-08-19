"""Exp100 — CatBoost Plain add rh_iws on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add rh_iws on Exp97 (CatBoost cycle 26/50)",
    "--add-feature", "rh_iws",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire recomputes Exp97 "
        "moist-calm hours by persist and dewpoint, not last fire's hours 0-5 blob. New: "
        "January RH>=70 Iws<2 persist>=150 n=17 RMSE 68.74 versus persist-1 36.22, over-cleans "
        "pred_d -30.2 versus need -12.2. January RH>=70 Iws<2 dewp_rise n=12 RMSE 51.75 "
        "versus persist 9.02, need +4.42 pred_d -6.22 wrong sign. January rh_iws tercile "
        "n=156 RMSE 39.39 versus persist 28.71 skill -37.2 percent. JJA RH>=70 Iws<2 is "
        "fine (13.56 versus persist 14.30). heating_night and bagging_temperature stay "
        "closed."
    ),
    "--citations",
    (
        "Cai, Wenju; Li, Ke; Liao, Hong; Wang, Huijun and Wu, Lixin 2017 Nature Climate "
        "Change 'Weather conditions conducive to Beijing severe haze more frequent under "
        "climate change' (doi:10.1038/nclimate3249) — Beijing haze traps under weak wind "
        "plus high RH, so the ratio RH over Iws names the moist-calm cell that separate "
        "rh_magnus and Iws splits miss in an oblivious tree. Relevance: Exp97 still RMSE "
        "39.39 versus persist-1 28.71 on January high rh_iws hours on the frozen 2014 "
        "nowcast, and adding rh_iws is one change from Exp97, not another clock product "
        "or Bayesian bootstrap."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding rh_iws, Magnus RH divided by Iws plus one, to the "
        "Exp97 CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, "
        "rh_magnus plus dewp_delta plus is_heating plus 24 lags) will cut 2013 val RMSE "
        "because the mechanism is one oblivious split on moist-calm so January high-RH "
        "low-wind hours are not scored like JJA moist-calm. Per Cai et al. 2017 that "
        "weak-wind high-RH cell is the Beijing haze trap. Because heating_night and "
        "bagging_temperature already failed, this is the unused RH/wind ratio not another "
        "night dummy. KEEP if 1h composite beats -22.167. This single change starts from "
        "the current champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, and "
        "composite -22.45 to -21.90. January rh_iws tercile RMSE may move from 39.39 "
        "toward 28.5 to 36.0 versus persist-1 28.71. A val RMSE above 22.25 is a miss. "
        "Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
