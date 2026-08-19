"""Exp120 — CatBoost Plain border_count=128 on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain border_count=128 on Exp97 (CatBoost cycle 46/50)",
    "--set", "border_count=128",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire does not retry "
        "Bernoulli subsample (Exp119 val 22.231). New: January PRES>=1025 n=428 is 16.5 "
        "percent of 2014 SSE, RMSE 36.25 versus persist 33.83, need +0.52 pred_d -5.60 "
        "(over-clean). Train 2011 PRES>=1025 is 34.7 percent versus 2013 val 24.4 and "
        "2014 25.9. Inversion mean train about 10.1 versus val 11.03 versus test 11.67. "
        "Keep dow and Bayesian bagging. Coarsen numeric borders."
    ),
    "--citations",
    (
        "Prokhorenkova, Liudmila; Gusev, Gleb; Vorobev, Aleksandr; Dorogush, Anna "
        "Veronika and Gulin, Andrey 2018 NeurIPS 'CatBoost: unbiased boosting with "
        "categorical features' (arXiv:1706.09516) — numeric features are quantized "
        "into a border grid before oblivious splits, so border_count caps how finely "
        "PRES and inversion can cut. Relevance: Exp119 Bernoulli subsample missed val, "
        "but January PRES>=1025 pred_d is -5.60 versus need +0.52 and 2011 has 34.7 "
        "percent high-PRES hours, so cutting border_count from 254 to 128 is one unused "
        "quantization change from Exp97, not another row-subsample."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting border_count from the CatBoost default 254 to 128 "
        "on the Exp97 CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, "
        "rh_magnus plus dewp_delta plus is_heating plus 24 lags plus dow plus is_weekend) "
        "will cut 2013 val RMSE because the mechanism is coarser PRES and inversion "
        "quantization so 2011 high-PRES winter hours cannot own fine leaves that "
        "over-clean January 2014. Per Prokhorenkova et al. 2018 that is border_count. "
        "Because Bernoulli subsample just failed, this is unused numeric quantization "
        "not another bagging knob. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. Val may move from 22.167 toward 21.90 to 22.20 "
        "if fine PRES borders were a 2013 tax. A val RMSE above 22.25 is a miss. Ranges "
        "are ug/m3 on the frozen timestamps."
    ),
])
