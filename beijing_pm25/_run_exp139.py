"""Exp139 — MLP add evening_peak on Exp136 recipe (MLP cycle 15/50)."""
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
    "--add-feature", "evening_peak",
    "--description", "MLP add evening_peak on Exp136 recipe (MLP cycle 15/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96, hour 20 32.19 need +7.65 pred_d +2.92, onset 110.39. New: "
        "weekday hours 18-21 n=939 RMSE 29.66 versus CatBoost 28.77 and persist 31.31, "
        "need +5.43 pred_d +2.67 so the net under-builds the commute pulse (24.7 percent "
        "of SSE). Hour 18-21 overall is 28.1 percent of SSE with pred_d +2.53 versus need "
        "+4.87. hour_sin and hour_cos already exist but smear a rectangular 4-hour spike. "
        "Add unused evening_peak, do not retry pres_delta."
    ),
    "--citations",
    (
        "Zheng, Yu; Liu, Furui and Hsieh, Hsun-Ping 2013 KDD 'U-Air: When Urban Air "
        "Quality Inference Meets Big Data' — Beijing PM2.5 has a sharp evening traffic "
        "and residential peak that they encode as a discrete time-of-day known input, "
        "not a smooth Fourier wave. Relevance: Exp136 already has hour_sin and hour_cos "
        "but weekday 18-21 still under-builds pred_d +2.67 versus need +5.43 and owns "
        "24.7 percent of SSE, so adding unused evening_peak is one commute dummy on the "
        "Exp136 recipe, not another weather derivative."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding evening_peak on the Exp136 MLP recipe (batch 16, "
        "hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, "
        "month_sin, pm25_accel, vent_index, Smooth-L1, Exp97 features plus a binary for "
        "hours 18-21) will cut 2013 val RMSE because the mechanism is an explicit commute "
        "dummy so weekday evening hours are not treated as a smeared hour_sin interpolation. "
        "Per Zheng et al. 2013 that is a discrete time-of-day known input. Because "
        "pres_delta just inverted 2013 val, this is unused evening_peak not another "
        "weather derivative. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.5 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.00, and composite -23.00 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if weekday-evening under-build was a 2013 tax. A val RMSE above "
        "22.85 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
