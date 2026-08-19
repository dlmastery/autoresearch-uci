"""Exp89 — CatBoost Plain add month_sin on Exp78 1h features."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add month_sin on Exp30 features (CatBoost cycle 15/50)",
    "--backbone", "catboost",
    "--add-feature", "month_sin",
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
        "persist-1 107.80. This fire recomputes Exp78 residuals on January calm hours, not "
        "last fire's hour-10 persist>=150 blob. Exp78 val 22.472 NEAR-MISS, test 21.058. "
        "New: January cv n=150 RMSE 33.27 versus Exp30 27.08 and persist-1 26.72. Hour 22 "
        "persist>=100 n=122 RMSE 30.49 versus Exp30 26.42 and persist 27.32. Exp78 has "
        "hour_sin/cos and dow but no month. Oblivious trees share January-calm leaves with "
        "July. l2=10 and Lossguide stay closed."
    ),
    "--citations",
    (
        "Zheng, Yu; Liu, Furui and Hsieh, Hsun-Ping 2013 KDD 'U-Air: When Urban Air Quality "
        "Inference Meets Big Data' (doi:10.1145/2487575.2488188) — they encode month as a "
        "cyclic feature so winter stagnation hours do not share a leaf with summer. "
        "Relevance: Exp78 CatBoost Plain still RMSE 33.27 versus persist-1 26.72 on January "
        "calm hours on the frozen 2014 nowcast, and adding month_sin is one change from "
        "Exp78, not the discarded is_heating dummy or another CatBoost HP."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding month_sin to the Exp78 CatBoost Plain recipe (depth 6, "
        "learning_rate 0.03, l2_leaf_reg 3, iterations 2000) with inversion_spread plus "
        "pm25_delta1 plus 24 lags otherwise unchanged will cut 2013 val RMSE because the "
        "mechanism is one oblivious winter split so January cv hours cannot share a persist "
        "leaf with July. Per Zheng et al. 2013 that is cyclic month. Because Lossguide and "
        "l2=10 already failed the val gate, this is a calendar feature rethink not another "
        "leaf penalty. KEEP if 1h composite beats -22.397. This single change starts from "
        "the current champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.7 to 22.2 versus Exp30 20.945, val 22.05 to 22.65, and "
        "composite -22.75 to -22.05. January cv RMSE may move from 33.27 toward 26 to 31 "
        "versus persist-1 26.72. A val RMSE above 22.55 is a miss. Ranges are ug/m3 on the "
        "frozen 2014 timestamps."
    ),
])
