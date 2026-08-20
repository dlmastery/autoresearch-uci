"""Exp160 — MLP drop is_weekend keep dow on Exp136 recipe (MLP cycle 36/50)."""
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
    "--drop-feature", "is_weekend",
    "--description", "MLP drop is_weekend keep dow on Exp136 recipe (MLP cycle 36/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96 versus JJA 13.96, hour 20 32.19, onset 110.39. Exp159 drop "
        "PRES missed val 22.437. New: Sat persist>=150 n=284 RMSE 34.51 versus CatBoost "
        "32.94, need -2.94 pred_d -4.25 (over-clean), while Sun persist>=150 n=227 RMSE "
        "31.83 versus 33.48, need -10.70 pred_d -8.52 (under-clean). is_weekend is a "
        "deterministic function of dow 5-6 (corr 0.79) that averages opposite "
        "Saturday-Sunday residuals. Keep dow. Drop unused is_weekend."
    ),
    "--citations",
    (
        "Cleveland, William S.; Graedel, T. E.; Kleiner, B. and Warner, J. L. 1974 "
        "Science 'Sunday and Workday Variations in Photochemical Air Pollutants in New "
        "Jersey and New York' — Sunday emission and photochemistry differ from Saturday, "
        "so a shared weekend dummy averages two regimes that numeric weekday already "
        "separates. Relevance: Exp136 already has numeric dow plus is_weekend, but Sat "
        "persist>=150 over-cleans pred_d -4.25 versus need -2.94 while Sun persist>=150 "
        "under-cleans pred_d -8.52 versus need -10.70, so dropping unused is_weekend "
        "while keeping dow is one calendar-collinear cleanup on the Exp136 recipe, not "
        "another weather drop."
    ),
    "--hypothesis",
    (
        "We hypothesize that dropping is_weekend while keeping numeric dow on the Exp136 "
        "MLP recipe (batch 16, hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, "
        "weight_decay 1e-4, log_iws, month_sin, pm25_accel, vent_index, Smooth-L1, "
        "clip=1.0) will cut 2013 val RMSE because the mechanism is removing a binary that "
        "forces Saturday and Sunday to share one first-layer weight so dirty Saturday "
        "hours are not over-cleaned while dirty Sunday hours under-clean. Per Cleveland "
        "et al. 1974 that is Sunday-versus-workday chemistry. Because drop PRES just "
        "missed val, this is unused drop-is_weekend not another weather drop. KEEP if 1h "
        "composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.6 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.10, and composite -23.10 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if the shared weekend dummy was a 2013 tax. A val RMSE above "
        "22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
