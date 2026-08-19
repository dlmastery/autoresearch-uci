"""Exp78 — CatBoost Plain (not Ordered) on Exp30 1h features."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain boosting on Exp30 inversion+delta features (CatBoost cycle 4/50)",
    "--backbone", "catboost",
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
        "persist-1 107.80. This fire recomputes Exp77 Ordered residuals, not last step's "
        "pre-run hour-20 January blob. Exp77 CatBoost Ordered test 21.520 val 23.190. "
        "New: hour-20 January RMSE 31.30 versus Exp30 27.61 (worse), need +11.8, pred -2.0 "
        "versus Exp30 +5.1. Onset increment flipped to -3.3 from Exp30 +0.2. persist>=150 "
        "typical RMSE 22.47 slightly beat Exp30 23.14 but pred -5.3 still over-cleans. "
        "Ordered past-only leaf averages shrank the lag-1 nowcast. t+6 Exp76 unchanged. "
        "LightGBM cycle stays closed."
    ),
    "--citations",
    (
        "Prokhorenkova, Liudmila; Gusev, Gleb; Vorobev, Aleksandr; Dorogush, Anna Veronika "
        "and Gulin, Andrey 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical "
        "Features' (arXiv:1706.09516) — Ordered boosting is for prediction shift on "
        "categorical target statistics; on purely numeric features they also report a Plain "
        "GBDT mode that uses the full gradient. Relevance: Exp77 Ordered onsets now predict "
        "-3.3 versus needed +87.4 on the frozen 2014 timestamps, worse than Exp30 LightGBM "
        "+0.2, so the numeric lag-1 nowcast is not a categorical-shift problem. Plain is "
        "one change from Exp77 Ordered, not a copy of discarded Exp21."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting boosting_type from Ordered to Plain on the Exp77 "
        "CatBoost (depth 6, learning_rate 0.03, l2_leaf_reg 3, iterations 2000) with the "
        "Exp30 inversion_spread plus pm25_delta1 plus 24-lag features unchanged will cut "
        "2013 val RMSE because the mechanism is full-gradient leaf values so lag-1 onsets "
        "are not shrunk by past-only permutation averages. Per Prokhorenkova et al. 2018 "
        "Plain is the numeric GBDT mode. Because Ordered just missed hour-20 January the "
        "wrong way, this is the Ordered-versus-Plain ablation not another depth. KEEP if "
        "1h composite beats -22.397. This single change starts from the current champion "
        "on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.7 to 22.3 versus Exp30 20.945, val 22.05 to 23.20, and "
        "composite -23.3 to -22.05. Hour-20 January RMSE may move from 31.30 toward 26 to "
        "30 versus Exp30 27.61. Onset increment may move from -3.3 toward -1 to +8 versus "
        "need +87.4. A val RMSE above 22.50 is a miss. Ranges are ug/m3 on the frozen 2014 "
        "timestamps."
    ),
])
