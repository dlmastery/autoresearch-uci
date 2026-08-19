"""Exp81 — isolated CatBoost Plain on Exp76 t+6 features."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain on Exp76 t+6 rh_magnus features (CatBoost cycle 7/50)",
    "--backbone", "catboost",
    "--data-path", str(HERE / "data" / "features_horizon6.csv"),
    "--add-feature", "month_sin",
    "--add-feature", "pres_delta",
    "--add-feature", "dewp_delta",
    "--add-feature", "cbwd_prev_NW",
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
        "persist-1 107.80. This fire recomputes Exp76 t+6 residuals on Saturday typical "
        "hours, not last fire's January persist>=150 1h blob. Exp76 val 57.161 test 54.312, "
        "gap 2.85. January 80.40 versus JJA 36.15. Hour 22 worst 64.43 (hour 20 63.03). "
        "Onset n=991 RMSE 91.18. New: Saturday typical n=830 RMSE 39.80 versus persist-6 "
        "24.07, skill -65.4 percent, need +3.3, pred +5.6. Weekday typical skill only "
        "-20.1 percent. 1h CatBoost lr and depth already taxed 2013 val. Ordered stays closed."
    ),
    "--citations",
    (
        "Prokhorenkova, Liudmila; Gusev, Gleb; Vorobev, Aleksandr; Dorogush, Anna Veronika "
        "and Gulin, Andrey 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical "
        "Features' (arXiv:1706.09516) — Plain oblivious trees share one split per level "
        "so a Saturday persist shard cannot get its own extra-trees linear slope. "
        "Relevance: Exp76 Saturday typical hours still RMSE 39.80 versus persist-6 24.07 "
        "on the frozen 2014 t+6 timestamps, skill -65.4 percent, and moving the Exp78 "
        "CatBoost Plain recipe onto those as-of-t-6 features is one isolated-backbone "
        "horizon change, not another 1h lr or depth after those taxed val."
    ),
    "--hypothesis",
    (
        "We hypothesize that training the Exp78 CatBoost Plain recipe (depth 6, "
        "learning_rate 0.03, l2_leaf_reg 3, iterations 2000) on the Exp76 t+6 feature "
        "set (month_sin plus pres_delta plus dewp_delta plus cbwd_prev_NW plus rh_magnus) "
        "will cut 2013 t+6 val RMSE because the mechanism is oblivious shared splits so "
        "Saturday typical persist hours cannot keep a private extra-trees linear increment. "
        "Per Prokhorenkova et al. 2018 that is Plain symmetric trees. Because 1h lr 0.01 "
        "and depth 4 already failed the val gate, this is a horizon rethink not another "
        "1h regularizer. The 1h composite will DISCARD; the side-ladder KEEP is t+6 val "
        "below 57.161. This single change starts from the current t+6 recipe on the frozen "
        "2014 test year."
    ),
    "--prediction",
    (
        "I predict t+6 test RMSE 53.5 to 58.5 versus Exp76 54.31, val 56.3 to 60.5, and "
        "1h-gate composite -61 to -53 (DISCARD). Saturday typical RMSE may move from 39.80 "
        "toward 26 to 36 versus persist-6 24.07. A val RMSE above 58.5 is a side-ladder "
        "miss. Ranges are ug/m3 on the frozen 2014 timestamps."
    ),
])
