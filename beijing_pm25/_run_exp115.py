"""Exp115 — CatBoost Plain drop pm25_lag13-24 on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
lags = ",".join(f"pm25_lag{k}" for k in range(13, 25))
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain drop pm25_lag13-24 on Exp97 (CatBoost cycle 41/50)",
    "--drop-feature", lags,
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire measures lag "
        "autocorrelation shift across splits, not last fire's Jan-Feb dummy. New: lag24 "
        "corr with y is 0.306 on 2013 val versus 0.397 on 2010-12 train and 0.440 on "
        "2014 test. lag12 is 0.509 val versus 0.558 train and 0.610 test. 2013 val "
        "persist 24.50 versus 2014 22.32; Exp97 skill is already +9.5 percent on val. "
        "Long lags help 2014 more than 2013. is_janfeb missed val. Calendar subsets, "
        "bomb-chasing, and weather increments stay closed."
    ),
    "--citations",
    (
        "Chen, Tianqi and Guestrin, Carlos 2016 KDD 'XGBoost: A Scalable Tree Boosting "
        "System' (arXiv:1603.02754) — extra correlated features increase tree complexity "
        "without new 1h signal, so dropping lag13-24 that are weaker in 2013 val "
        "(lag24 corr 0.306 versus train 0.397) is a regularizer against 2010-12 "
        "multi-day episode memory. Relevance: 2013 val persist is 24.50 versus 2014 test "
        "22.32 and long-lag autocorrelation is the split that favors 2014 over 2013, and "
        "truncating the lag window to 12h is one change from Exp97, not another Jan-Feb "
        "dummy after is_janfeb missed 2013 val."
    ),
    "--hypothesis",
    (
        "We hypothesize that dropping pm25_lag13 through pm25_lag24 from the Exp97 "
        "CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, rh_magnus "
        "plus dewp_delta plus is_heating plus lags 1-12) will cut 2013 val RMSE because "
        "the mechanism is removing 2010-12 multi-day episode memory that is weaker in "
        "2013 so val is not pulled toward 2014-like long-memory leaves. Per Chen and "
        "Guestrin 2016 extra correlated features overfit. Because is_janfeb just failed, "
        "this is unused lag-window truncation not another calendar flag. KEEP if 1h "
        "composite beats -22.167. This single change starts from the current champion "
        "on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.6 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. Val may move from 22.167 toward 21.90 to 22.20 "
        "if 2013 long-lag mismatch was the tax. A val RMSE above 22.25 is a miss. "
        "Ranges are ug/m3 on the frozen timestamps."
    ),
])
