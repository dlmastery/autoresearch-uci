"""Exp95 — CatBoost Plain random_strength=2 on Exp91 rh_magnus 1h recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain random_strength=2 on Exp91 rh_magnus (CatBoost cycle 21/50)",
    "--backbone", "catboost",
    "--add-feature", "rh_magnus",
    "--set", "iterations=2000",
    "--set", "depth=6",
    "--set", "learning_rate=0.03",
    "--set", "l2_leaf_reg=3",
    "--set", "early_stopping_rounds=100",
    "--set", "boosting_type=Plain",
    "--set", "random_strength=2",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp94 residuals, not the pre-run high-PRES "
        "blob. Exp94 DISCARD val 22.528 test 21.063. New: hiP dirty no-NW n=277 RMSE 43.66 "
        "versus Exp91 43.72 flat versus persist 38.64. Previous-NW hours 45.37 to 42.75 so "
        "the dummy helped the wrong hours. cv persist>=150 29.15 to 29.57 worse. Still "
        "over-cleans hiP dirty pred_d -9.35 versus need -3.2. random_strength is still 1 "
        "on 1h Plain. cbwd_prev_NW stays closed."
    ),
    "--citations",
    (
        "Prokhorenkova, Liudmila; Gusev, Gleb; Vorobev, Aleksandr; Dorogush, Anna Veronika "
        "and Gulin, Andrey 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical "
        "Features' (arXiv:1706.09516) — random_strength adds Gaussian noise to split "
        "scores so persist plus PRES cannot always win the same cleanout cut on 2010-2012 "
        "high-pressure dirty shards. Relevance: Exp94 still RMSE 43.66 versus persist-1 "
        "38.64 on PRES>=1025 persist>=150 hours with no previous-hour NW on the frozen "
        "2014 nowcast, and random_strength=2 is one change from Exp91, not another wind "
        "dummy after cbwd_prev_NW taxed val."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting random_strength from 1 to 2 on the Exp91 CatBoost "
        "Plain recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, rh_magnus plus "
        "inversion_spread plus pm25_delta1 plus 24 lags, no cbwd_prev_NW) will cut 2013 "
        "val RMSE because the mechanism is noisier split scores so oblivious trees cannot "
        "lock the same high-PRES cleanout cut that over-predicts a 9 ug drop. Per "
        "Prokhorenkova et al. 2018 that is random_strength. Because cbwd_prev_NW just "
        "helped the wrong hours, this is split-score noise not another wind dummy. KEEP "
        "if 1h composite beats -22.397. This single change starts from the current "
        "champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.6 to 21.8 versus Exp30 20.945, val 22.05 to 22.60, and "
        "composite -22.70 to -22.05. PRES>=1025 persist>=150 RMSE may move from 44.27 "
        "toward 40.0 to 43.5 versus persist-1 40.56. A val RMSE above 22.55 is a miss. "
        "Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
