"""Exp77 — isolated CatBoost start: Ordered boosting on Exp30 1h features."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Ordered boosting on Exp30 inversion+delta features (CatBoost cycle 3/50)",
    "--backbone", "catboost",
    "--set", "iterations=2000",
    "--set", "depth=6",
    "--set", "learning_rate=0.03",
    "--set", "l2_leaf_reg=3",
    "--set", "early_stopping_rounds=100",
    "--set", "boosting_type=Ordered",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 is worst at 31.93. This fire recomputes "
        "Exp30 residuals on hour-20 January and dirty-typical hours, not last fire's t+6 "
        "persist>=250 over-clean. Onset actual-lag1>50 n=83 RMSE 110.05 loses to persist-1 "
        "107.80, need +87.4, pred +0.2. New: hour-20 January n=29 RMSE 27.61 versus persist "
        "25.29, skill -9.2 percent. persist>=150 typical |delta|<=50 n=1490 RMSE 23.14 versus "
        "persist 19.34, skill -19.6 percent, pred -4.7 versus need +0.1. LightGBM 50/50 is "
        "snapshotted. t+6 Exp76 stays a side ladder (val 57.161). Isolated CatBoost starts "
        "on these Exp30 features; Exp21 lacked inversion_spread."
    ),
    "--citations",
    (
        "Prokhorenkova, Liudmila; Gusev, Gleb; Vorobev, Aleksandr; Dorogush, Anna Veronika "
        "and Gulin, Andrey 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical "
        "Features' (arXiv:1706.09516) — ordered boosting scores each example from a past-only "
        "permutation so a January haze hour cannot leak into its own leaf value. Relevance: "
        "Exp30 hour-20 January still loses to persist (skill -9.2 percent) and persist>=150 "
        "typical hours predict -4.7 versus need +0.1 on the frozen 2014 nowcast, which is the "
        "prediction shift ordered boosting was designed to stop. This is the isolated CatBoost "
        "start on Exp30 inversion+delta features, not the discarded Exp21 drive-by."
    ),
    "--hypothesis",
    (
        "We hypothesize that switching the Exp30 1h recipe from LightGBM to CatBoost with "
        "Prokhorenkova Ordered boosting (depth 6, learning_rate 0.03, l2_leaf_reg 3, "
        "iterations 2000), leaving the inversion_spread plus pm25_delta1 plus 24-lag feature "
        "set unchanged, will cut 2013 val RMSE because the mechanism is past-only residual "
        "estimates so leaf values cannot reuse the same 2010-2012 January hour-20 haze "
        "episodes LightGBM scores greedily. Per Prokhorenkova et al. 2018 that is ordered "
        "boosting. Because LightGBM 50/50 is closed and Exp21 lacked inversion_spread, this "
        "is the isolated CatBoost paper start not another LightGBM knob. KEEP if 1h composite "
        "beats -22.397. This single change starts from the current champion on the frozen "
        "2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.8 to 22.5 versus Exp30 20.945, val 22.10 to 23.40, and "
        "composite -23.5 to -22.05. Hour-20 January RMSE may move from 27.61 toward 24 to "
        "27 versus persist 25.29. persist>=150 typical increment may move from -4.7 toward "
        "-3 to +1 versus need +0.1. A val RMSE above 22.50 is a miss. Ranges are ug/m3 on "
        "the frozen 2014 timestamps."
    ),
])
