"""Exp148 — MLP extra hidden 256-128-64-32 on Exp136 recipe (MLP cycle 24/50)."""
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
    "--set", "hidden=[256,128,64,32]",
    "--add-feature", "log_iws",
    "--add-feature", "month_sin",
    "--add-feature", "pm25_accel",
    "--add-feature", "vent_index",
    "--description", "MLP extra hidden 256-128-64-32 on Exp136 recipe (MLP cycle 24/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96 versus JJA 13.96, hour 20 32.19, onset 110.39. Extra-feature "
        "adds Exp137-147 all DISCARD. New: evening 18-21 persist>=150 n=246 RMSE 39.89 "
        "versus CatBoost 38.09 and persist 44.60, need +3.80 pred_d +1.92 so the 3-layer "
        "net under-ramps nested evening haze (11.7 percent of SSE). Width 128-64-32 already "
        "inverted. Add unused extra hidden 32, do not retry cv_inv."
    ),
    "--citations",
    (
        "Montufar, Guido F.; Pascanu, Razvan; Cho, Kyunghyun and Bengio, Yoshua 2014 "
        "NeurIPS 'On the Number of Linear Regions of Deep Neural Networks' "
        "(arXiv:1312.6098) — a deep rectifier net's piecewise-linear regions grow "
        "exponentially in depth but only polynomially in width, so one extra layer buys "
        "nested partitions that extra units cannot. Relevance: Exp136 is a 3-layer "
        "256-128-64 GELU trunk and evening persist>=150 still loses CatBoost 39.89 versus "
        "38.09 with pred_d +1.92 versus need +3.80, width shrink already failed, so adding "
        "unused hidden 32 is one extra composition stage on the Exp136 recipe, not another "
        "feature or nearby width."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting hidden from 256-128-64 to 256-128-64-32 on the "
        "Exp136 MLP recipe (batch 16, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, "
        "log_iws, month_sin, pm25_accel, vent_index, Smooth-L1, Exp97 features plus one "
        "unused 32-unit layer) will cut 2013 val RMSE because the mechanism is one extra "
        "composition stage so evening persist>=150 hours are not treated as additive "
        "hour_sin plus lag1. Per Montufar et al. 2014 that is depth-driven linear regions. "
        "Because extra-feature adds 137-147 all failed and width shrink already inverted, "
        "this is unused depth not another feature or nearby width. KEEP if 1h composite "
        "beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.6 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.10, and composite -23.10 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if missing evening-haze composition was a 2013 tax. A val RMSE "
        "above 22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
