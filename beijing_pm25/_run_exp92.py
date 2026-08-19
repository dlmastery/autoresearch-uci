"""Exp92 — CatBoost Plain rh_magnus plus l2_leaf_reg=10 on Exp91."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain rh_magnus l2=10 on Exp91 (CatBoost cycle 18/50)",
    "--backbone", "catboost",
    "--add-feature", "rh_magnus",
    "--set", "iterations=2000",
    "--set", "depth=6",
    "--set", "learning_rate=0.03",
    "--set", "l2_leaf_reg=10",
    "--set", "early_stopping_rounds=100",
    "--set", "boosting_type=Plain",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp91 rh_magnus residuals, not last step's "
        "pre-run low-PRES blob. Exp91 val 22.449 beat Exp78 22.472 and is 0.052 from Exp30 "
        "22.397 (inside seed plus-or-minus 0.08). Test 21.045. New after RH: PRES<1010 "
        "persist>=150 RMSE 31.25 to 29.82 versus persist 30.51 and Exp30 27.53. Hour-22 "
        "persist>=100 30.49 to 29.77. Exp88 l2=10 won 2014 test 20.80 but val 22.488. "
        "Stacking l2=10 onto Exp91 is one change. month_sin and accel stay closed."
    ),
    "--citations",
    (
        "Prokhorenkova, Liudmila; Gusev, Gleb; Vorobev, Aleksandr; Dorogush, Anna Veronika "
        "and Gulin, Andrey 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical "
        "Features' (arXiv:1706.09516) — l2_leaf_reg shrinks oblivious-leaf values once the "
        "feature set is fixed. Relevance: Exp91 rh_magnus still sits 0.052 val above Exp30 "
        "on the frozen 2014 nowcast after the low-PRES dirty slice moved 31.25 to 29.82, "
        "and l2=10 is one change from Exp91, not a retry of Exp88 without RH."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting l2_leaf_reg from 3 to 10 on the Exp91 CatBoost Plain "
        "recipe (depth 6, learning_rate 0.03, rh_magnus plus inversion_spread plus "
        "pm25_delta1 plus 24 lags) will cut 2013 val RMSE because the mechanism is stronger "
        "leaf L2 so the new RH splits cannot overfit 2010-2012 low-PRES shards. Per "
        "Prokhorenkova et al. 2018 that is l2_leaf_reg. Because Exp91 just became the "
        "CatBoost val leader and Exp88 l2=10 won test, this is shrink on the RH recipe not "
        "another feature. KEEP if 1h composite beats -22.397. This single change starts "
        "from the current champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.6 to 21.8 versus Exp30 20.945, val 22.05 to 22.60, and "
        "composite -22.70 to -22.05. PRES<1010 persist>=150 RMSE may move from 29.82 toward "
        "27.5 to 30.0 versus Exp30 27.53. A val RMSE above 22.55 is a miss. Ranges are "
        "ug/m3 on the frozen 2014 timestamps."
    ),
])
