"""Exp79 — CatBoost Plain lr 0.03 to 0.01 on Exp30 features."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain learning_rate 0.01 on Exp30 features (CatBoost cycle 5/50)",
    "--backbone", "catboost",
    "--set", "iterations=2000",
    "--set", "depth=6",
    "--set", "learning_rate=0.01",
    "--set", "l2_leaf_reg=3",
    "--set", "early_stopping_rounds=100",
    "--set", "boosting_type=Plain",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp78 Plain residuals on January dirty-typical "
        "and hour-10, not last fire's hour-20 January blob. Exp78 val 22.472 test 21.058. "
        "New: January persist>=150 typical n=149 RMSE 40.32 versus Exp30 31.84 and persist "
        "20.81, pred -13.0 versus need -0.8. Hour 10 overall RMSE 25.23 versus Exp30 21.40 "
        "and persist 22.86. January hour 22 RMSE 46.37 versus Exp30 34.49, pred -5.3 versus "
        "need +6.8. January Iws<2 RMSE 34.02 versus Exp30 28.65. lr 0.03 is three times "
        "Exp30 LightGBM 0.01. Ordered stays closed."
    ),
    "--citations",
    (
        "Dorogush, Anna Veronika; Ershov, Vasily and Gulin, Andrey 2018 arXiv 'CatBoost: "
        "gradient boosting with categorical features support' (arXiv:1810.11363) — they "
        "train Plain symmetric trees with a small learning rate and many iterations so "
        "each tree is a weak shrink of the persist residual. Relevance: Exp78 Plain at "
        "lr 0.03 still over-cleans January persist>=150 typical hours (pred -13.0 versus "
        "need -0.8) on the frozen 2014 nowcast, and cutting lr to 0.01 is one change from "
        "Exp78, not the discarded Ordered run or a copy of Exp26 that lacked inversion."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting learning_rate from 0.03 to 0.01 on the Exp78 CatBoost "
        "Plain recipe (depth 6, l2_leaf_reg 3, iterations 2000, boosting_type Plain) with "
        "the Exp30 inversion_spread plus pm25_delta1 plus 24-lag features unchanged will "
        "cut 2013 val RMSE because the mechanism is slower shrinkage so symmetric depth-6 "
        "trees cannot slam January persist>=150 typical hours down by 13. Per Dorogush et "
        "al. 2018 that is a small learning rate with many trees. Because Ordered is closed "
        "and hour-20 January already improved, this is the unused shrink on the January "
        "dirty-typical hole. KEEP if 1h composite beats -22.397. This single change starts "
        "from the current champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.7 to 22.2 versus Exp30 20.945, val 22.05 to 22.70, and "
        "composite -22.8 to -22.05. January persist>=150 typical RMSE may move from 40.32 "
        "toward 28 to 36 versus Exp30 31.84, and increment from -13.0 toward -8 to -3 versus "
        "need -0.8. A val RMSE above 22.55 is a miss. Ranges are ug/m3 on the frozen 2014 "
        "timestamps."
    ),
])
