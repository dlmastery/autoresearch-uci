"""Exp104 — CatBoost Plain min_data_in_leaf=20 on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain min_data_in_leaf=20 on Exp97 (CatBoost cycle 30/50)",
    "--set", "min_data_in_leaf=20",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire recomputes Exp97 "
        "January by weekday, not last fire's onset dPRES blob. New: January weekday n=520 "
        "holds 21.0 percent of SSE, RMSE 37.18 versus Exp30 34.88 and persist-1 33.67 "
        "(skill -10.4 percent), over-cleans pred_d -4.86 versus need +0.35. January "
        "weekend n=169 RMSE 26.39 versus persist 33.29 (skill +20.7 percent). January "
        "Friday n=120 RMSE 50.59 versus persist 46.70. CatBoost default min_data_in_leaf "
        "is 1. pres_delta Depthwise and heating products stay closed."
    ),
    "--citations",
    (
        "Ke, Guolin; Meng, Qi; Finley, Thomas; Wang, Taifeng; Chen, Wei; Ma, Weidong; "
        "Ye, Qiwei and Liu, Tie-Yan 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient "
        "Boosting Decision Tree' (arXiv:1706.08359) — min_data_in_leaf is the count "
        "floor that stops a booster from isolating a handful of 2010-2012 weekday-haze "
        "hours; CatBoost exposes the same floor and defaults it to 1. Relevance: Exp97 "
        "still RMSE 37.18 versus persist-1 33.67 on January weekday hours that hold 21 "
        "percent of 2014 SSE on the frozen nowcast, and min_data_in_leaf=20 is one "
        "change from Exp97, not the discarded LGB min_data=100 run or another weather "
        "tendency."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting min_data_in_leaf from 1 to 20 on the Exp97 CatBoost "
        "Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, rh_magnus plus "
        "dewp_delta plus is_heating plus 24 lags) will cut 2013 val RMSE because the "
        "mechanism is a larger leaf floor so weekday-January 2010-2012 haze hours cannot "
        "own an oblivious leaf that over-cleans 2013. Per Ke et al. 2017 that is "
        "min_data_in_leaf. Because pres_delta just failed, this is the unused CatBoost "
        "leaf floor not another derivative. KEEP if 1h composite beats -22.167. This "
        "single change starts from the current champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, and "
        "composite -22.45 to -21.90. January weekday RMSE may move from 37.18 toward "
        "33.5 to 36.5 versus persist-1 33.67. A val RMSE above 22.25 is a miss. Ranges "
        "are ug/m3 on the frozen 2014 timestamps."
    ),
])
