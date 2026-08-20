"""Exp142 — MLP add is_severe on Exp136 recipe (MLP cycle 18/50)."""
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
    "--add-feature", "is_severe",
    "--description", "MLP add is_severe on Exp136 recipe (MLP cycle 18/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96, hour 20 32.19, onset 110.39. New: lag1>=250 still-rising "
        "n=276 RMSE 33.74 versus CatBoost 38.98 and persist 29.76, need +21.38 pred_d "
        "-1.96 so the net predicts a drop while mega-haze is still building (9.4 percent "
        "of SSE). z-scored lag1 smears the 250 breakpoint. Add unused is_severe, do not "
        "retry pm25_delta6."
    ),
    "--citations",
    (
        "Cheng, Yafang; Zheng, Guangjie; Wei, Chao; Mu, Qing; Zheng, Bo; Wang, Zhibin; "
        "Gao, Meng; Zhang, Qiang; He, Kebin; Carmichael, Gregory; Poschl, Ulrich and Su, "
        "Hang 2016 Science Advances 'Reactive nitrogen chemistry in aerosol water as a "
        "source of sulfate during haze events in China' (doi:10.1126/sciadv.1601530) — "
        "severe haze is a distinct aqueous-chemistry regime, not a linear interpolation "
        "of moderate hours. Relevance: Exp136 already has continuous lag1 but rising "
        "lag1>=250 hours still predict -1.96 versus need +21.38 and lose persist 33.74 "
        "versus 29.76, so adding unused is_severe is one HJ-633 breakpoint dummy on the "
        "Exp136 recipe, not another 6h PM slope."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding is_severe on the Exp136 MLP recipe (batch 16, hidden "
        "256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, month_sin, "
        "pm25_accel, vent_index, Smooth-L1, Exp97 features plus lag1>=250) will cut 2013 "
        "val RMSE because the mechanism is an explicit severe-haze regime flag so "
        "still-rising mega-haze hours are not treated as mean-reverting moderate persist. "
        "Per Cheng et al. 2016 that is a distinct chemical regime. Because pm25_delta6 "
        "just inverted 2013 val, this is unused is_severe not another 6h PM slope. KEEP "
        "if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.5 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.00, and composite -23.00 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if rising-severe mean-reversion was a 2013 tax. A val RMSE above "
        "22.85 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
