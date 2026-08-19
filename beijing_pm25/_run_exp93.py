"""Exp93 — CatBoost Plain rsm=0.8 on Exp91 rh_magnus 1h recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain rsm=0.8 on Exp91 rh_magnus (CatBoost cycle 19/50)",
    "--backbone", "catboost",
    "--add-feature", "rh_magnus",
    "--set", "iterations=2000",
    "--set", "depth=6",
    "--set", "learning_rate=0.03",
    "--set", "l2_leaf_reg=3",
    "--set", "early_stopping_rounds=100",
    "--set", "boosting_type=Plain",
    "--set", "rsm=0.8",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp91 residuals on hour 10, not last fire's "
        "low-PRES dirty blob. Exp91 val 22.449 is 0.052 from KEEP. New: hour 10 RMSE 23.95 "
        "versus Exp30 21.40 and persist-1 22.86 (skill -4.8 percent). Hour 22 20.95 versus "
        "persist 20.19. January cv still 32.53 versus persist 26.72. rsm default 1 lets "
        "persist plus RH sit in every oblivious level. l2=10 on RH already taxed val. "
        "Exp30 LightGBM uses feature_fraction 0.8."
    ),
    "--citations",
    (
        "Prokhorenkova, Liudmila; Gusev, Gleb; Vorobev, Aleksandr; Dorogush, Anna Veronika "
        "and Gulin, Andrey 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical "
        "Features' (arXiv:1706.09516) — rsm is the per-tree column subsample so persist "
        "cannot appear at every oblivious level. Relevance: Exp91 hour-10 still RMSE 23.95 "
        "versus persist-1 22.86 on the frozen 2014 nowcast, and rsm=0.8 is one change from "
        "Exp91 matching the Exp30 feature_fraction, not another leaf L2."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting rsm from 1.0 to 0.8 on the Exp91 CatBoost Plain recipe "
        "(depth 6, learning_rate 0.03, l2_leaf_reg 3, rh_magnus plus inversion_spread plus "
        "pm25_delta1 plus 24 lags) will cut 2013 val RMSE because the mechanism is 80 percent "
        "column subsample so hour-10 mixing can split on Iws when persist is held out. Per "
        "Prokhorenkova et al. 2018 that is rsm. Because l2=10 already failed val, this is "
        "feature-wise bagging not another leaf penalty. KEEP if 1h composite beats -22.397. "
        "This single change starts from the current champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.6 to 21.8 versus Exp30 20.945, val 22.05 to 22.60, and "
        "composite -22.70 to -22.05. Hour-10 RMSE may move from 23.95 toward 21.2 to 23.0 "
        "versus persist-1 22.86. A val RMSE above 22.55 is a miss. Ranges are ug/m3 on the "
        "frozen 2014 timestamps."
    ),
])
