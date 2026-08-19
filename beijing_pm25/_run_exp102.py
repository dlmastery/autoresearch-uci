"""Exp102 — CatBoost Plain grow_policy=Depthwise on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain grow_policy=Depthwise on Exp97 (CatBoost cycle 28/50)",
    "--set", "grow_policy=Depthwise",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire recomputes Exp97 "
        "error share, not last fire's aggregate building-dirty blob. New: January is 8.7 "
        "percent of hours but 24.5 percent of SSE. January persist>=150 delta1>0 and "
        "PRES>=1025 n=52 is 0.7 percent of hours and 7.2 percent of SSE, RMSE 68.80 "
        "versus persist-1 47.75, need +13.38 pred_d -18.48 wrong sign. heating_build "
        "worsened that shard to 71.97. not-January persist>=150 delta1>0 beats persist "
        "(29.41 versus 32.76). Three interaction products failed. Lossguide is closed."
    ),
    "--citations",
    (
        "Prokhorenkova, Liudmila; Gusev, Gleb; Vorobev, Aleksandr; Dorogush, Anna Veronika "
        "and Gulin, Andrey 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical "
        "Features' (arXiv:1706.09516) — grow_policy Depthwise expands one child at a "
        "time with a node-specific split so a 0.7 percent high-loss January high-PRES "
        "building-dirty shard can own a path, unlike oblivious SymmetricTree. Relevance: "
        "Exp97 still RMSE 68.80 versus persist-1 47.75 on that 52-hour shard on the "
        "frozen 2014 nowcast, and Depthwise is one change from Exp97, not another "
        "hand-built product after heating_build failed."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting grow_policy from SymmetricTree to Depthwise on the "
        "Exp97 CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, "
        "rh_magnus plus dewp_delta plus is_heating plus 24 lags) will cut 2013 val RMSE "
        "because the mechanism is node-specific splits so the 52-hour January high-PRES "
        "building-dirty shard is not forced to share every oblivious cut. Per "
        "Prokhorenkova et al. 2018 that is Depthwise. Because heating_build just failed "
        "and Lossguide already closed, this is the unused grow policy not another "
        "product. KEEP if 1h composite beats -22.167. This single change starts from the "
        "current champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, and "
        "composite -22.45 to -21.90. January persist>=150 delta1>0 PRES>=1025 RMSE may "
        "move from 68.80 toward 48.0 to 64.0 versus persist-1 47.75. A val RMSE above "
        "22.25 is a miss. Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
