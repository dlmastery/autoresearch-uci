"""Exp90 — CatBoost Plain add pm25_accel on Exp78 1h features."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add pm25_accel on Exp30 features (CatBoost cycle 16/50)",
    "--backbone", "catboost",
    "--add-feature", "pm25_accel",
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
        "persist-1 107.80. This fire recomputes Exp89 month_sin residuals, not last step's "
        "pre-run January cv blob. Exp89 val 22.708 worse than Exp78 22.472, test 21.056. "
        "January cv 32.97 still versus persist 26.72. JJA 14.11 taxed versus Exp78 13.98. "
        "Cyclic month is closed. New unused curvature: pm25_accel is in features_full but "
        "not in Exp78. Exp38 LightGBM accel was a 1h NEAR-MISS DISCARD; CatBoost never "
        "tried it. Lossguide and l2=10 stay closed."
    ),
    "--citations",
    (
        "Ke, Guolin; Meng, Qi; Finley, Thomas; Wang, Taifeng; Chen, Wei; Ma, Weidong; "
        "Ye, Qiwei and Liu, Tie-Yan 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient "
        "Boosting Decision Tree' (arXiv:1706.08359) — a cheap extra numeric column is one "
        "leaf-wise or oblivious split; second-difference accel is lag1-2*lag2+lag3. "
        "Relevance: Exp78 CatBoost still RMSE 33.27 on January cv versus persist 26.72 on "
        "the frozen 2014 nowcast after month_sin taxed JJA, and adding pm25_accel is one "
        "change from Exp78, not the discarded 1h LightGBM Exp38 copy of HPs."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding pm25_accel equals lag1 minus twice lag2 plus lag3 to "
        "the Exp78 CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, "
        "iterations 2000) with inversion_spread plus pm25_delta1 plus 24 lags otherwise "
        "unchanged will cut 2013 val RMSE because the mechanism is one oblivious split on "
        "curvature so already-decelerating persist hours are not treated as still-building. "
        "Per Ke et al. 2017 that split is cheap. Because month_sin just taxed JJA, this is "
        "momentum not another calendar dummy. KEEP if 1h composite beats -22.397. This "
        "single change starts from the current champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.7 to 22.2 versus Exp30 20.945, val 22.05 to 22.70, and "
        "composite -22.8 to -22.05. January cv RMSE may move from 33.27 toward 27 to 32 "
        "versus persist-1 26.72. A val RMSE above 22.55 is a miss. Ranges are ug/m3 on the "
        "frozen 2014 timestamps."
    ),
])
