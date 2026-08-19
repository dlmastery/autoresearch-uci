"""Exp80 — CatBoost Plain depth 6 to 4 on Exp78 lr=0.03 recipe."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain depth 4 on Exp30 features (CatBoost cycle 6/50)",
    "--backbone", "catboost",
    "--set", "iterations=2000",
    "--set", "depth=4",
    "--set", "learning_rate=0.03",
    "--set", "l2_leaf_reg=3",
    "--set", "early_stopping_rounds=100",
    "--set", "boosting_type=Plain",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp79 lr=0.01 residuals on the January "
        "dirty-typical hole, not last step's pre-run hour-10 blob. Exp79 val 22.587 lost "
        "to Exp78 22.472. New after shrink: January persist>=150 typical n=149 RMSE 37.55 "
        "(was 40.32) still worse than Exp30 31.84, pred -11.4 versus need -0.8. Hour 10 "
        "24.45 still worse than Exp30 21.40. January hour 22 39.77 still worse than 34.49. "
        "lr 0.01 moved the increment the right way but hurt 2013 val. Depth 6 symmetric "
        "trees still isolate persist shards. Ordered and lr 0.01 stay closed."
    ),
    "--citations",
    (
        "Prokhorenkova, Liudmila; Gusev, Gleb; Vorobev, Aleksandr; Dorogush, Anna Veronika "
        "and Gulin, Andrey 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical "
        "Features' (arXiv:1706.09516) — Plain mode grows oblivious depth-d trees so depth "
        "4 has 16 shared splits instead of 64, which cannot isolate a 2010-2012 January "
        "persist>=150 shard. Relevance: Exp79 at depth 6 still predicts -11.4 versus need "
        "-0.8 on January persist>=150 typical hours on the frozen 2014 nowcast, and depth "
        "4 is one change from Exp78, not the discarded lr=0.01 run or XGBoost Exp2."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting depth from 6 to 4 on the Exp78 CatBoost Plain recipe "
        "(learning_rate 0.03, l2_leaf_reg 3, iterations 2000, boosting_type Plain) with "
        "the Exp30 inversion_spread plus pm25_delta1 plus 24-lag features unchanged will "
        "cut 2013 val RMSE because the mechanism is 16 oblivious leaves instead of 64 so "
        "January persist>=150 typical hours cannot get their own -13 increment. Per "
        "Prokhorenkova et al. 2018 that is symmetric-tree depth. Because lr 0.01 already "
        "failed the val gate, this is a capacity cut not another shrink. KEEP if 1h "
        "composite beats -22.397. This single change starts from the current champion on "
        "the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.7 to 22.3 versus Exp30 20.945, val 22.05 to 22.75, and "
        "composite -22.9 to -22.05. January persist>=150 typical RMSE may move from 40.32 "
        "toward 29 to 37 versus Exp30 31.84, and increment from -13.0 toward -9 to -2 versus "
        "need -0.8. A val RMSE above 22.60 is a miss. Ranges are ug/m3 on the frozen 2014 "
        "timestamps."
    ),
])
