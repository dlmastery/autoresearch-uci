"""Exp101 — CatBoost Plain add heating_build on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add heating_build on Exp97 (CatBoost cycle 27/50)",
    "--add-feature", "heating_build",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire recomputes Exp97 "
        "January persist>=150 by momentum, not last fire's rh_iws blob. New: January "
        "persist>=150 and pm25_delta1>0 n=109 RMSE 53.00 versus persist-1 39.20 (skill "
        "-35.2 percent), need +4.82 pred_d -6.04 wrong sign. January persist>=150 already "
        "falling (delta1<0) has skill +10.6 percent. January persist>=150 PRES>=1025 n=88 "
        "RMSE 68.58 versus persist 60.04, pred_d -30.1 versus need -9.1. January persist>=150 "
        "TEMP<0 n=129 RMSE 49.41 versus persist 38.29. rh_iws heating_night and T=2 stay "
        "closed."
    ),
    "--citations",
    (
        "Prokhorenkova, Liudmila; Gusev, Gleb; Vorobev, Aleksandr; Dorogush, Anna Veronika "
        "and Gulin, Andrey 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical "
        "Features' (arXiv:1706.09516) — oblivious trees reuse one split per level so "
        "is_heating and pm25_delta1 cannot form the winter-building interaction unless "
        "that product is an explicit column. Relevance: Exp97 still RMSE 53.00 versus "
        "persist-1 39.20 on January persist>=150 hours with rising first difference on "
        "the frozen 2014 nowcast, and adding heating_build is one change from Exp97, not "
        "another RH/Iws ratio."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding heating_build, is_heating times max of pm25_delta1 "
        "and zero, to the Exp97 CatBoost Plain recipe (depth 6, learning_rate 0.03, "
        "l2_leaf_reg 3, rh_magnus plus dewp_delta plus is_heating plus 24 lags) will cut "
        "2013 val RMSE because the mechanism is one oblivious split on winter building "
        "so January persist>=150 rising hours are not scored like already-falling dirty "
        "hours. Per Prokhorenkova et al. 2018 that product is the interaction oblivious "
        "trees cannot form. Because rh_iws already failed, this is winter momentum not "
        "another wind ratio. KEEP if 1h composite beats -22.167. This single change "
        "starts from the current champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, and "
        "composite -22.45 to -21.90. January persist>=150 delta1>0 RMSE may move from "
        "53.00 toward 39.5 to 49.0 versus persist-1 39.20. A val RMSE above 22.25 is a "
        "miss. Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
