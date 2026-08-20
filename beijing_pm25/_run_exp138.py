"""Exp138 — MLP add pres_delta on Exp136 recipe (MLP cycle 14/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--backbone", "mlp",
    "--set", "weight_decay=0.0001",
    "--set", "batch_size=16",
    "--add-feature", "log_iws",
    "--add-feature", "month_sin",
    "--add-feature", "pm25_accel",
    "--add-feature", "vent_index",
    "--add-feature", "pres_delta",
    "--description", "MLP add pres_delta on Exp136 recipe (MLP cycle 14/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96, hour 20 32.19, onset 110.39. New: collapse hours with "
        "dPRES>=1 n=51 RMSE 86.12 versus CatBoost 80.04 and persist 107.64, need -91.41 "
        "pred_d -24.29 so the net under-cleans 67 ug of a synoptic crash (11.3 percent of "
        "SSE versus 9.6 percent of Exp97). dPRES>=1 persist>=150 collapse n=35 RMSE 97.53 "
        "versus CatBoost 88.82. PRES is already a column but a 1 hPa hour is about 0.1 "
        "sigma after z-score. Add unused pres_delta, do not retry roll6max."
    ),
    "--citations",
    (
        "Cai, Wenju; Li, Ke; Liao, Hong; Wang, Huijun and Wu, Lixin 2017 Nature Climate "
        "Change 'Weather conditions conducive to Beijing severe haze more frequent under "
        "climate change' (doi:10.1038/nclimate3249) — Beijing haze sits in a stagnant "
        "synoptic regime and is flushed when that pattern breaks, so hourly surface "
        "pressure tendency is the transition clock a z-scored PRES level does not name. "
        "Relevance: Exp136 already has PRES but collapse dPRES>=1 still under-cleans "
        "pred_d -24.29 versus need -91.41 and owns 11.3 percent of SSE, so adding unused "
        "pres_delta is one synoptic-tendency feature on the Exp136 recipe, not another "
        "rolling PM statistic."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding pres_delta on the Exp136 MLP recipe (batch 16, "
        "hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, "
        "month_sin, pm25_accel, vent_index, Smooth-L1, Exp97 features plus one-hour PRES "
        "difference) will cut 2013 val RMSE because the mechanism is an explicit pressure "
        "tendency so collapse hours during a rising high are not treated like stagnant "
        "PRES-level persist. Per Cai et al. 2017 that is a synoptic-regime break. Because "
        "roll6max just inverted 2013 val, this is unused pres_delta not another rolling "
        "PM statistic. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.5 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.00, and composite -23.00 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if collapse-on-rising-pressure under-clean was a 2013 tax. A val "
        "RMSE above 22.85 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
