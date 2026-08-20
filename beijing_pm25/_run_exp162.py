"""Exp162 — MLP drop is_heating keep month_sin on Exp136 recipe (MLP cycle 38/50)."""
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
    "--drop-feature", "is_heating",
    "--description", "MLP drop is_heating keep month_sin on Exp136 recipe (MLP cycle 38/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96 versus JJA 13.96, hour 20 32.19, onset 110.39. Exp161 drop "
        "inversion missed val 22.487. New: Feb persist>=150 n=262 RMSE 34.20 versus "
        "CatBoost 31.39 and persist 33.74, need -2.03 pred_d -7.89 so the heating dummy "
        "over-cleans February dirty hours. is_heating-month_sin corr is only 0.20 while "
        "is_heating-TEMP is -0.77. Keep month_sin. Drop unused is_heating."
    ),
    "--citations",
    (
        "Zhang, Qiang; He, Kebin and Huo, Hong 2012 Nature 'Cleaning China's air' — "
        "northern winter coal heating is not a flat November-February plateau, so a "
        "binary heating dummy forces February to share January's first-layer weight even "
        "though coal load and mixing differ by month. Relevance: Exp136 already has "
        "month_sin plus TEMP with is_heating corr -0.77, but Feb persist>=150 still "
        "over-cleans pred_d -7.89 versus need -2.03 at 34.20 versus CatBoost 31.39, so "
        "dropping unused is_heating while keeping month_sin is one calendar-step cleanup "
        "on the Exp136 recipe, not another inversion drop."
    ),
    "--hypothesis",
    (
        "We hypothesize that dropping is_heating while keeping month_sin on the Exp136 "
        "MLP recipe (batch 16, hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, "
        "weight_decay 1e-4, log_iws, pm25_accel, vent_index, Smooth-L1, clip=1.0) will "
        "cut 2013 val RMSE because the mechanism is removing a Nov-Feb step dummy so "
        "February dirty hours are not scored with January's over-clean weight while "
        "month_sin and TEMP still mark winter. Per Zhang et al. 2012 that is month-varying "
        "coal heating. Because drop inversion_spread just missed val, this is unused "
        "drop-is_heating not another moisture drop. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.6 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.10, and composite -23.10 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if the shared heating dummy was a 2013 tax. A val RMSE above "
        "22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
