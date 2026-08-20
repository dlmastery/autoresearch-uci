"""Exp143 — MLP add cbwd_prev_NW on Exp136 recipe (MLP cycle 19/50)."""
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
    "--add-feature", "cbwd_prev_NW",
    "--description", "MLP add cbwd_prev_NW on Exp136 recipe (MLP cycle 19/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96, hour 20 32.19, onset 110.39. New: just-left-NW hours "
        "n=522 Iws mean 1.95 RMSE 20.07 versus persist 22.63, need -3.70 pred_d -1.03 so "
        "the net forgets residual cleanout after Iws resets (6.3 percent of SSE). "
        "persist>=150 subset n=97 need -13.98 pred_d -5.32. Current cbwd_NW is already 0. "
        "Add unused cbwd_prev_NW, do not retry is_severe."
    ),
    "--citations",
    (
        "Zheng, Yu; Yi, Xiuwen; Li, Ming; Li, Ruiyuan; Shan, Zhangqing; Chang, Eric and "
        "Li, Tianrui 2015 KDD 'Forecasting Fine-Grained Air Quality Based on Big Data' — "
        "their Beijing forecast treats sudden meteorological transitions, not weather "
        "levels, as the regime switch a contemporaneous dummy misses after Iws resets. "
        "Relevance: Exp136 already has cbwd_NW, Iws, log_iws, and vent_index but "
        "just-left-NW hours still under-clean pred_d -1.03 versus need -3.70 with Iws "
        "mean 1.95, so adding unused previous-hour NW is one transition-memory feature "
        "on the Exp136 recipe, not another lag1 threshold."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding cbwd_prev_NW on the Exp136 MLP recipe (batch 16, "
        "hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, "
        "month_sin, pm25_accel, vent_index, Smooth-L1, Exp97 features plus last-hour NW "
        "dummy) will cut 2013 val RMSE because the mechanism is explicit fetch memory "
        "after Iws resets so just-left-NW hours are not treated as calm stagnant air. "
        "Per Zheng et al. 2015 that is a meteorological transition. Because is_severe "
        "just inverted rising mega-haze, this is unused cbwd_prev_NW not another lag1 "
        "flag. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.5 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.00, and composite -23.00 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if Iws-reset under-clean was a 2013 tax. A val RMSE above 22.85 "
        "is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
