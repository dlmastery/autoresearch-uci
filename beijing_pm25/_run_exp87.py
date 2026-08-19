"""Exp87 — CatBoost Plain Lossguide on Exp78 1h features."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain grow_policy=Lossguide on Exp30 features (CatBoost cycle 13/50)",
    "--backbone", "catboost",
    "--set", "iterations=2000",
    "--set", "depth=6",
    "--set", "learning_rate=0.03",
    "--set", "l2_leaf_reg=3",
    "--set", "early_stopping_rounds=100",
    "--set", "boosting_type=Plain",
    "--set", "grow_policy=Lossguide",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp78 Plain residuals on hour-10 dirty "
        "hours, not last fire's t+6 wrong-sign blob. Exp78 val 22.472 NEAR-MISS versus "
        "22.397, test 21.058. New: hour-10 persist>=150 n=70 RMSE 48.03 versus Exp30 38.25 "
        "and persist-1 40.22. Hour-10 collapses n=6 RMSE 147.97 versus Exp30 103.27, pred "
        "+2.2 versus need -113.7. Hour-10 Iws>=5 n=146 RMSE 33.13 versus Exp30 26.19. "
        "Oblivious depth-6 shares persist splits with night hours. 1h Ordered, lr 0.01, "
        "and depth 4 stay closed."
    ),
    "--citations",
    (
        "Ke, Guolin; Meng, Qi; Finley, Thomas; Wang, Taifeng; Chen, Wei; Ma, Weidong; "
        "Ye, Qiwei and Liu, Tie-Yan 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient "
        "Boosting Decision Tree' (arXiv:1706.08359) — leaf-wise growth isolates a rare "
        "hour-10 persist-plus-wind leaf that oblivious symmetric trees cannot cut. "
        "Relevance: Exp78 CatBoost Plain still RMSE 48.03 versus persist-1 40.22 on hour-10 "
        "persist>=150 hours on the frozen 2014 nowcast, and grow_policy=Lossguide is one "
        "change from Exp78, not the discarded 1h Ordered run or another depth."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting grow_policy from SymmetricTree to Lossguide on the "
        "Exp78 CatBoost Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, "
        "iterations 2000) with the Exp30 inversion_spread plus pm25_delta1 plus 24-lag "
        "features unchanged will cut 2013 val RMSE because the mechanism is leaf-wise "
        "splits so hour-10 persist>=150 collapse hours can own an Iws-plus-persist leaf. "
        "Per Ke et al. 2017 that is leaf-wise growth. Because Ordered, lr 0.01, and depth "
        "4 already failed, this is an architecture rethink not another nearby HP. KEEP if "
        "1h composite beats -22.397. This single change starts from the current champion "
        "on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.7 to 22.3 versus Exp30 20.945, val 22.05 to 22.70, and "
        "composite -22.8 to -22.05. Hour-10 persist>=150 RMSE may move from 48.03 toward "
        "38 to 44 versus Exp30 38.25. A val RMSE above 22.55 is a miss. Ranges are ug/m3 "
        "on the frozen 2014 timestamps."
    ),
])
