"""Exp119 — CatBoost Plain Bernoulli subsample=0.8 on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain Bernoulli subsample=0.8 on Exp97 (CatBoost cycle 45/50)",
    "--set", "bootstrap_type=Bernoulli",
    "--set", "subsample=0.8",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire does not touch "
        "model_size_reg (Exp118 was bit-identical). New: hour 1 RMSE 29.32 versus persist "
        "28.19. 2013 val hour-1 need is -2.18 (overnight fall) versus 2014 +1.45 and "
        "2010/2012 about +2.0. January hour-1 n=28 RMSE 74.63 versus persist 69.40, need "
        "+8.32 pred_d -5.90 (wrong sign), 4.6 percent of all 2014 SSE. Keep dow. "
        "Regularize overnight leaves with row subsample."
    ),
    "--citations",
    (
        "Chen, Tianqi and Guestrin, Carlos 2016 KDD 'XGBoost: A Scalable Tree Boosting "
        "System' (arXiv:1603.02754) — row subsample is stochastic gradient boosting so "
        "no single train-year hour can own every tree. Relevance: Exp118 model_size_reg=1.0 "
        "was bit-identical, but 2013 hour-1 need is -2.18 while 2014 is +1.45 and January "
        "hour-1 pred_d is -5.90 versus need +8.32, so Bernoulli subsample 0.8 is one "
        "unused CatBoost bagging change from Exp97, not another weak leaf-size HP."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting bootstrap_type to Bernoulli with subsample 0.8 on "
        "the Exp97 CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, "
        "rh_magnus plus dewp_delta plus is_heating plus 24 lags plus dow plus is_weekend) "
        "will cut 2013 val RMSE because the mechanism is stochastic rows so 2013 "
        "overnight-fall hour-1 shards cannot own every oblivious tree that then "
        "over-cleans January 2014. Per Chen and Guestrin 2016 that is subsample. Because "
        "model_size_reg=1.0 was inert, this is unused Bernoulli bagging not another "
        "leaf-size knob. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. Val may move from 22.167 toward 21.90 to 22.20 "
        "if 2013 hour-1 fall was a tax. A val RMSE above 22.25 is a miss. Ranges are "
        "ug/m3 on the frozen timestamps."
    ),
])
