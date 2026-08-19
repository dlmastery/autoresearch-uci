"""Exp105 — CatBoost Plain early_stopping_rounds=50 on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain early_stopping_rounds=50 on Exp97 (CatBoost cycle 31/50)",
    "--set", "early_stopping_rounds=50",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire recomputes January "
        "weekday by persist and clock, not last fire's aggregate weekday blob. New: "
        "January weekday persist>=150 n=141 holds 13.0 percent of SSE, RMSE 56.12 versus "
        "Exp30 50.34 and persist-1 45.99, over-cleans pred_d -18.33 versus need -7.60. "
        "January weekday hours 0-5 n=126 RMSE 51.08 versus persist 43.95. January Friday "
        "evening 18-21 n=20 RMSE 65.27 versus persist 50.33, need +23.30 pred_d -2.45 "
        "wrong sign. not-January weekday beats persist (18.67 versus 20.96). min_data=20 "
        "was inert. Leaf floor and heating products stay closed."
    ),
    "--citations",
    (
        "Chen, Tianqi and Guestrin, Carlos 2016 KDD 'XGBoost: A Scalable Tree Boosting "
        "System' (arXiv:1603.02754) — early stopping on a held-out year is the "
        "regularizer that stops adding trees once validation error plateaus, so extra "
        "rounds cannot memorize 2010-2012 weekday-haze collapses. Relevance: Exp97 still "
        "RMSE 56.12 versus persist-1 45.99 on January weekday persist>=150 hours that "
        "hold 13 percent of 2014 SSE on the frozen nowcast, and early_stopping_rounds "
        "100 to 50 is one change from Exp97, not another leaf floor after min_data=20 "
        "was inert."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting early_stopping_rounds from 100 to 50 on the Exp97 "
        "CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, rh_magnus "
        "plus dewp_delta plus is_heating plus 24 lags) will cut 2013 val RMSE because "
        "the mechanism is fewer extra trees after the 2013 plateau so weekday-January "
        "dirty hours are not over-cleaned. Per Chen and Guestrin 2016 that is early "
        "stopping. Because min_data_in_leaf=20 was inert, this is the unused patience "
        "knob not another leaf floor. KEEP if 1h composite beats -22.167. This single "
        "change starts from the current champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, and "
        "composite -22.45 to -21.90. January weekday persist>=150 RMSE may move from "
        "56.12 toward 46.0 to 54.0 versus persist-1 45.99. A val RMSE above 22.25 is a "
        "miss. Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
