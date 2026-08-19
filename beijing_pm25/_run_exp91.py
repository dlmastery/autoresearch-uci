"""Exp91 — CatBoost Plain add rh_magnus on Exp78 1h features."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add rh_magnus on Exp30 features (CatBoost cycle 17/50)",
    "--backbone", "catboost",
    "--add-feature", "rh_magnus",
    "--set", "iterations=2000",
    "--set", "depth=6",
    "--set", "learning_rate=0.03",
    "--set", "l2_leaf_reg=3",
    "--set", "early_stopping_rounds=100",
    "--set", "boosting_type=Plain",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp78 residuals on low-PRES dirty hours "
        "and hour 22, not last fire's January cv blob. Exp78 val 22.472 NEAR-MISS, test "
        "21.058. New: PRES<1010 persist>=150 n=273 RMSE 31.25 versus Exp30 27.53 and "
        "persist-1 30.51. Hour-22 persist>=100 n=122 RMSE 30.49 versus Exp30 26.42 and "
        "persist 27.32. inversion_spread is linear; Magnus RH is unused on 1h CatBoost. "
        "month_sin and accel stay closed."
    ),
    "--citations",
    (
        "Tie, Xuexi; Huang, Ru-Jin; Cao, Junji; Zhang, Qiang; Cheng, Yafang; Su, Hang; "
        "Chang, Di; Poeschl, Ulrich; Hoffmann, Thorsten; Dusek, Ulrike; Li, Guohui; "
        "Worsnop, Douglas R. and O'Dowd, Colin D. 2017 Nature Scientific Reports "
        "'Severe Pollution in China Amplified by Atmospheric Moisture' "
        "(doi:10.1038/s41598-017-11457-w) — falling pressure with rising RH marks moist "
        "inflow that inversion_spread smears. Relevance: Exp78 still RMSE 31.25 versus "
        "persist-1 30.51 on PRES<1010 persist>=150 hours on the frozen 2014 nowcast, and "
        "adding rh_magnus is one change from Exp78, not the discarded month_sin or accel."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding rh_magnus, Magnus-Tetens RH from TEMP and DEWP, to the "
        "Exp78 CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, "
        "iterations 2000) with inversion_spread plus pm25_delta1 plus 24 lags otherwise "
        "unchanged will cut 2013 val RMSE because the mechanism is one oblivious split on "
        "nonlinear humidity so low-PRES dirty hours are not treated as dry-high-PRES haze. "
        "Per Tie et al. 2017 that moisture state amplifies PM. Because month_sin and accel "
        "already failed, this is the unused physical RH feature not another lag. KEEP if "
        "1h composite beats -22.397. This single change starts from the current champion "
        "on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.7 to 22.2 versus Exp30 20.945, val 22.05 to 22.65, and "
        "composite -22.75 to -22.05. PRES<1010 persist>=150 RMSE may move from 31.25 toward "
        "27 to 30 versus Exp30 27.53. A val RMSE above 22.55 is a miss. Ranges are ug/m3 "
        "on the frozen 2014 timestamps."
    ),
])
