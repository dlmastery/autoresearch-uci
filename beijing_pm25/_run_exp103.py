"""Exp103 — CatBoost Plain add pres_delta on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add pres_delta on Exp97 (CatBoost cycle 29/50)",
    "--add-feature", "pres_delta",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48 "
        "beats persist 33.24, onset n=83 RMSE 110.06 losing to persist-1 107.80 with "
        "pred_d -0.28 versus need +87.4. This fire recomputes onset by pressure tendency, "
        "not last fire's 52-hour high-PRES shard. New: onset hours with dPRES>=1 n=20 "
        "hold 14.7 percent of SSE, RMSE 158.68 versus persist-1 156.02, need +119 pred_d "
        "-0.96. Onset dPRES<=-1 is only 3.9 percent of SSE. corr of pres_delta with the "
        "1h increment on onset hours is 0.34 versus about 0 globally. Depthwise Lossguide "
        "and heating products stay closed."
    ),
    "--citations",
    (
        "Zheng, Yu; Yi, Xiuwen; Li, Ming; Li, Ruiyuan; Shan, Zhangqing; Chang, Eric and "
        "Li, Tianrui 2015 KDD 'Forecasting Fine-Grained Air Quality Based on Big Data' "
        "— sudden meteorological transitions, especially pressure rises that mark "
        "synoptic onsets, drive the largest hourly PM jumps and need an explicit "
        "tendency column. Relevance: Exp97 still RMSE 158.68 versus persist-1 156.02 on "
        "the 20 onset hours with dPRES>=1 that hold 14.7 percent of 2014 SSE on the "
        "frozen nowcast, and adding pres_delta is one change from Exp97, not another "
        "grow policy after Depthwise failed."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding pres_delta, the 1h PRES difference, to the Exp97 "
        "CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, rh_magnus "
        "plus dewp_delta plus is_heating plus 24 lags) will cut 2013 val RMSE because "
        "the mechanism is one oblivious split on rising pressure so onset hours with "
        "dPRES>=1 are not scored like typical near-zero increments. Per Zheng et al. "
        "2015 that synoptic tendency drives the jump. Because Depthwise just failed, "
        "this is the unused 1h pressure clock not another grow policy. KEEP if 1h "
        "composite beats -22.167. This single change starts from the current champion "
        "on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, and "
        "composite -22.45 to -21.90. Onset dPRES>=1 RMSE may move from 158.68 toward "
        "140.0 to 156.0 versus persist-1 156.02. A val RMSE above 22.25 is a miss. "
        "Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
